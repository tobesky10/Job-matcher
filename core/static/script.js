/*
// Elements
const jobListEl = document.getElementById('job-list');
const paginationEl = document.getElementById('pagination');
const jobSearchEl = document.getElementById('job-search');
const spinnerEl = document.getElementById('spinner');
const resumeForm = document.getElementById('resume-form');
const resumeTextEl = document.getElementById('resume-text');
const matchResultsEl = document.getElementById('match-results');
const jobsErrorEl = document.getElementById('jobs-error');
const resumeErrorEl = document.getElementById('resume-error');
const nlptokenEL = document.getElementById('nlptoken');

const JOBS_PER_PAGE = 10;
let jobs = [];
let filteredJobs = [];
let currentPage = 1;

// Show/hide spinner
function showSpinner() {
  spinnerEl.classList.remove('hidden');
  spinnerEl.setAttribute('aria-busy', 'true');
}

function hideSpinner() {
  spinnerEl.classList.add('hidden');
  spinnerEl.setAttribute('aria-busy', 'false');
}

// Show/hide error messages
function showError(element, message) {
  element.textContent = message;
  element.classList.remove('hidden');
}

function hideError(element) {
  element.classList.add('hidden');
  element.textContent = '';
}



// Fetch job listings from API or static source
/*async function fetchJobs() {
  showSpinner();
  hideError(jobsErrorEl);
  try {
    // Example: Replace with your actual API endpoint
    const response = await fetch('http://localhost:8000/core/parse-resume/');
    if (!response.ok) throw new Error('Failed to fetch jobs');
    const data = await response.json();
    jobs = data.jobs || [];
    filteredJobs = jobs;
    currentPage = 1;
    renderJobs();
  } catch (error) {
    showError(jobsErrorEl, 'Unable to load job listings. Please try again later.');
    console.error(error);
  } finally {
    hideSpinner();
  }
}*/
/*
// Render jobs for current page
function renderJobs() {
  const start = (currentPage - 1) * JOBS_PER_PAGE;
  const end = start + JOBS_PER_PAGE;
  const jobsToShow = filteredJobs.slice(start, end);

  if (jobsToShow.length === 0) {
    jobListEl.innerHTML = '<p>No jobs found.</p>';
    paginationEl.innerHTML = '';
    return;
  }

  jobListEl.innerHTML = jobsToShow.map(job => `
    <div class="job-item" tabindex="0">
      <h3>${escapeHtml(job.title)}</h3>
      <p>${escapeHtml(job.description || '')}</p>
      <p><strong>Location:</strong> ${escapeHtml(job.location || 'N/A')}</p>
    </div>
  `).join('');

  renderPaginationControls();
}

// Render pagination buttons
function renderPaginationControls() {
  const totalPages = Math.ceil(filteredJobs.length / JOBS_PER_PAGE);
  paginationEl.innerHTML = '';

  if (totalPages <= 1) return;

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement('button');
    btn.textContent = i;
    btn.disabled = i === currentPage;
    btn.setAttribute('aria-label', `Go to page ${i}`);
    btn.addEventListener('click', () => {
      currentPage = i;
      renderJobs();
      // Move focus to job list for accessibility
      jobListEl.focus();
    });
    paginationEl.appendChild(btn);
  }
}

// Filter jobs based on search input
function filterJobs(query) {
  const q = query.trim().toLowerCase();
  if (!q) {
    filteredJobs = jobs;
  } else {
    filteredJobs = jobs.filter(job =>
      job.title.toLowerCase().includes(q) ||
      (job.description && job.description.toLowerCase().includes(q)) ||
      (job.location && job.location.toLowerCase().includes(q))
    );
  }
  currentPage = 1;
  renderJobs();
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
  if (!text) return '';
  return text.replace(/[&<>"']/g, function (m) {
    return {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    }[m];
  });
}

// Save resume text to localStorage
function saveResumeText(text) {
  localStorage.setItem('resumeText', text);
}

// Load resume text from localStorage
function loadResumeText() {
  const saved = localStorage.getItem('resumeText');
  if (saved) {
    resumeTextEl.value = saved;
  }
}

// Save match results to localStorage
function saveMatchResults(results) {
  localStorage.setItem('matchResults', JSON.stringify(results));
}

// Load match results from localStorage
function loadMatchResults() {
  const saved = localStorage.getItem('matchResults');
  if (saved) {
    try {
      const results = JSON.parse(saved);
      renderMatchResults(results);
    } catch {
      // Ignore parse errors
    }
  }
}

// Render match results
function renderMatchResults(results) {
  if (!results || results.length === 0) {
    matchResultsEl.innerHTML = '<p>No matches found.</p>';
    return;
  }
  matchResultsEl.innerHTML = results.map(match => `
    <div class="job-item" tabindex="0">
      <h3>${escapeHtml(match.title)}</h3>
      <p>${escapeHtml(match.description || '')}</p>
      <p><strong>Location:</strong> ${escapeHtml(match.location || 'N/A')}</p>
      <p><strong>Match Score:</strong> ${match.score ? match.score.toFixed(2) : 'N/A'}</p>
    </div>
  `).join('');
}

// Handle resume form submission
async function handleResumeSubmit(event) {
  event.preventDefault();
  hideError(resumeErrorEl);
  matchResultsEl.innerHTML = '';
  const resumeText = resumeTextEl.value.trim();

  if (!resumeText) {
    showError(resumeErrorEl, 'Please enter your resume text.');
    return;
  }

  saveResumeText(resumeText);

  showSpinner();

  try {
    // Replace with your actual API endpoint and payload
    const response = await fetch('http://localhost:8000/core/parse-resume/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ resume: resumeText })
    });

    if (!response.ok) throw new Error('Failed to match jobs');

    const data = await response.json();

    if (!data.matches || data.matches.length === 0) {
      matchResultsEl.innerHTML = '<p>No matching jobs found.</p>';
      saveMatchResults([]);
    } else {
      renderMatchResults(data.matches);
      saveMatchResults(data.matches);
    }
  } catch (error) {
    showError(resumeErrorEl, 'Error matching jobs. Please try again later.');
    console.error(error);
  } finally {
    hideSpinner();
  }
}

// Smooth scrolling for navigation links
function enableSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
}

// Initialize app
function init() {
  loadResumeText();
  loadMatchResults();
  fetchJobs();

  jobSearchEl.addEventListener('input', e => {
    filterJobs(e.target.value);
  });

  resumeForm.addEventListener('submit', handleResumeSubmit);

  enableSmoothScrolling();
}

// Run init on DOMContentLoaded
document.addEventListener('DOMContentLoaded', init);
*/

document.getElementById('resume-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const resumeText = document.getElementById('resume-text').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('http://localhost:8000/core/parse-resume/',  {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ resume_text: resumeText })
    })
    .then(response => response.json())
    .then(data => {
        if (data.skills) {
            document.getElementById('skills-result').innerHTML =
                '<strong>Extracted Skills:</strong> ' + data.skills.join(', ');
        } else if (data.error) {
            document.getElementById('skills-result').innerHTML =
                '<span style="color:red;">' + data.error + '</span>';
        }

        if (data.tokens) {
            document.getElementById('tokens-result').innerHTML =
                '<strong>Tokens:</strong> ' + data.tokens.join(', ');
        }
    })
    .catch(() => {
        document.getElementById('skills-result').innerHTML =
            '<span style="color:red;">An error occurred.</span>';
    });
});
