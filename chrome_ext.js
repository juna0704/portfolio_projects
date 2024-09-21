// manifest.json
{
  "manifest_version": 2,
  "name": "Website Technology Detector",
  "version": "1.0",
  "description": "Detects technologies used by websites",
  "permissions": [
    "activeTab",
    "http://*/*",
    "https://*/*"
  ],
  "browser_action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icon16.png",
      "48": "icon48.png",
      "128": "icon128.png"
    }
  },
  "icons": {
    "16": "icon16.png",
    "48": "icon48.png",
    "128": "icon128.png"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"]
    }
  ]
}

// popup.html
<!DOCTYPE html>
<html>
<head>
  <title>Website Technology Detector</title>
  <style>
    body { width: 300px; padding: 10px; }
    ul { padding-left: 20px; }
  </style>
</head>
<body>
  <h2>Detected Technologies:</h2>
  <ul id="techList"></ul>
  <script src="popup.js"></script>
</body>
</html>

// popup.js
document.addEventListener('DOMContentLoaded', function() {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {action: "detectTechnologies"}, function(response) {
      const techList = document.getElementById('techList');
      response.technologies.forEach(function(tech) {
        const li = document.createElement('li');
        li.textContent = tech;
        techList.appendChild(li);
      });
    });
  });
});

// content.js
function detectTechnologies() {
  const technologies = [];

  // Check if the content is dynamic
  const initialHTML = document.documentElement.outerHTML;
  setTimeout(() => {
    if (initialHTML !== document.documentElement.outerHTML) {
      technologies.push("Dynamic Website");
    } else {
      technologies.push("Static Website");
    }
  }, 1000);

  // Check for common frameworks
  if (document.querySelector('[ng-app], [ng-controller]')) technologies.push("AngularJS");
  if (document.querySelector('[data-reactroot], [data-react-id]')) technologies.push("React");
  if (document.querySelector('[data-v-]')) technologies.push("Vue.js");

  // Check for AJAX requests
  const originalXHR = window.XMLHttpRequest;
  let ajaxDetected = false;
  window.XMLHttpRequest = function() {
    ajaxDetected = true;
    return new originalXHR();
  };
  setTimeout(() => {
    if (ajaxDetected) technologies.push("AJAX");
    window.XMLHttpRequest = originalXHR;
  }, 1000);

  // Check for Single Page Application (SPA)
  const originalPushState = history.pushState;
  let spaDetected = false;
  history.pushState = function() {
    spaDetected = true;
    return originalPushState.apply(this, arguments);
  };
  setTimeout(() => {
    if (spaDetected) technologies.push("Single Page Application (SPA)");
    history.pushState = originalPushState;
  }, 1000);

  // Check for server-side rendering
  if (document.documentElement.innerHTML.includes('server-side-render')) {
    technologies.push("Server-side Rendering");
  }

  // Check for common libraries
  if (window.jQuery) technologies.push("jQuery");
  if (document.documentElement.innerHTML.includes('bootstrap')) technologies.push("Bootstrap");

  return technologies;
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "detectTechnologies") {
    sendResponse({technologies: detectTechnologies()});
  }
});