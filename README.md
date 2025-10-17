<h1 style="border-bottom: 3px solid #007bff; padding-bottom: 10px;">🎓 STUDENT FEEDBACK PORTAL</h1>
<p>This is a Streamlit web application designed to collect and manage student feedback for academic sessions, workshops, or courses. It utilizes a MySQL database for persistent storage and offers two separate interfaces: Student (for submission) and Admin (for management and data export).</p>
<hr>

<h2>1. FEATURES</h2>
<ul>
    <li><strong>Dual Interface:</strong> Separate login/access points for Students (to submit feedback) and Administrators (to manage sessions and view data).</li>
    <li><strong>Session Management:</strong> Admins can easily add new sessions (defined by Session Name, Resource Person, and Topic).</li>
    <li><strong>Data Persistence:</strong> All session definitions and submitted feedback are stored in a MySQL database.</li>
    <li><strong>Secure Admin Access:</strong> The Admin Panel is protected by a password configured via environment variables or Streamlit secrets.</li>
    <li><strong>Data Export:</strong> Admins can view all submitted feedback and download the data as a CSV file for analysis.</li>
</ul>
<hr>

<h2>2. PREREQUISITES</h2>
<p>You need to have the following installed and set up to run this application:</p>
<ul>
<li>Python 3.8+</li>
<li><strong>Streamlit</strong> (<code>pip install streamlit</code>)</li>
<li><strong>Pandas</strong> (<code>pip install pandas</code>)</li>
<li><strong>MySQL Connector</strong> (<code>pip install mysql-connector-python</code>)</li>
<li>A running <strong>MySQL database</strong> instance.</li>
</ul>

<hr>

<h2>3. SETUP AND CONFIGURATION</h2>

<h3>3.1. Database Setup</h3>
<p>The application expects a MySQL database and two tables. You must create them before running the app. The default database name is <code>feed</code>.</p>

<h4>A. <code>sessions</code> Table:</h4>
<p>Stores details of the available sessions for feedback.</p>
<pre><code>CREATE TABLE sessions (
id INT AUTO_INCREMENT PRIMARY KEY,
session_name VARCHAR(255) NOT NULL,
resource_person VARCHAR(255) NOT NULL,
topic VARCHAR(255) NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);</code></pre>

<h4>B. <code>feedback</code> Table:</h4>
<p>Stores the actual feedback submissions from students.</p>
<pre><code>CREATE TABLE feedback (
id INT AUTO_INCREMENT PRIMARY KEY,
    session_name VARCHAR(255) NOT NULL,
    student_name VARCHAR(255) NOT NULL,
    usn VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    resource_person VARCHAR(255) NOT NULL,
    topic VARCHAR(255) NOT NULL,
    rating INT NOT NULL,
    feedback TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);</code></pre>


<h3>3.2. Configuration (Environment Variables / Streamlit Secrets)</h3>
<p>Configure your database credentials and the admin password using environment variables.</p>

<table>
    <thead>
        <tr>
            <th>Variable</th>
            <th>Description</th>
            <th>Default Value in Code</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>DB_HOST</strong></td>
            <td>MySQL Host Address</td>
            <td><code>localhost</code></td>
        </tr>
        <tr>
            <td><strong>DB_USER</strong></td>
            <td>MySQL User</td>
            <td><code>root</code></td>
        </tr>
        <tr>
            <td><strong>DB_PASSWORD</strong></td>
            <td>MySQL Password</td>
            <td><code>Chandu@123</code> (<strong>MUST CHANGE</strong>)</td>
        </tr>
        <tr>
            <td><strong>DB_NAME</strong></td>
            <td>MySQL Database Name</td>
            <td><code>feed</code></td>
        </tr>
        <tr>
            <td><strong>ADMIN_PASSWORD</strong></td>
            <td>Password for Admin Login</td>
            <td>(Must be set)</td>
        </tr>
    </tbody>
</table>

<p>You can set <code>ADMIN_PASSWORD</code> as an environment variable or in your Streamlit secrets file (<code>.streamlit/secrets.toml</code>):</p>
<pre><code># .streamlit/secrets.toml
[admin]
password = "YourSecureAdminPasswordHere"</code></pre>

<hr>

<h2>4. HOW TO RUN</h2>
<p>Execute the Python file using Streamlit:</p>
<pre><code>streamlit run app_file_name.py</code></pre>
<p>(Replace <code>app_file_name.py</code> with your Python script name.)</p>

<hr>

<h2>5. USAGE GUIDE</h2>

<h3>STUDENT ROLE:</h3>
<ol>
    <li>Select the <strong>Session</strong>, <strong>Resource Person</strong>, and <strong>Topic</strong> from the dropdowns.</li>
    <li>Fill in required personal details (Name, USN, Email).</li>
    <li>Set a <strong>Rating</strong> (1-5) and provide detailed <strong>Feedback</strong>.</li>
    <li>Click <strong>Submit Feedback</strong>.</li>
</ol>

<h3>ADMIN ROLE:</h3>
<ol>
    <li>Switch to the Admin role in the sidebar and enter the <strong>Admin Password</strong> to log in.</li>
    <li><strong>Add New Session:</strong> Use the input fields to define a new session and make it available for students to review.</li>
    <li><strong>View Submitted Feedback:</strong> Filter the data by session and use the <strong>Download Feedback as CSV</strong> button to export the collected results.</li>
</ol>

<hr>

