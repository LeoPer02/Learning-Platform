## Final Project - Secure Learning Platform

### Scenario

Your organization, specializing in software security, plans to host a web learning platform to enhance its security training content for employees and to offer public tutorials on its SecDevOps products. The platform must be secure to maintain the company's reputation. Your team, part of the secure software development group, is tasked with designing and implementing this secure solution.

### Project Components

The learning platform will be a modern web application with two main components:

- **Client:** A web frontend for company employees to create, manage, and configure courses, accessible to other employees and the general public.
- **Server:** A backend with REST endpoints accessible by the client and advanced users.

### General Requirements

#### Interface
- **Course Management:**
  - Create, configure, edit, and delete courses.
  - Each course includes a listing of topics.
  - Topics can be in draft (owner-visible) or published (public or restricted).
  - Forums for enrolled users to discuss topics, with support for anonymous or authenticated submissions and file uploads.
  - Personal page for each student listing enrolled courses.

#### Authentication
- Non-anonymous users must authenticate to access the platform.
- Minimal authentication (e.g., password-based) and secure communications (e.g., HTTPS) are required.
- Focus on overall security rather than cryptographic protocol details.

#### Access Control
- Only administrators can create/delete courses.
- Course owners manage content and enrollment.
- Courses can be private (with enrolled students) or public (accessible to anyone).
- Only enrolled students can access and post in private courses.

### Design

Your team will design the software components and security mechanisms, adopting a SecDevOps approach. This includes system architecture, actor specification, use/misuse cases, and threat identification, following guidelines from the NIST Secure Software Development Framework and the OWASP Web Security Testing Guide.

### Implementation

Develop a functional learning platform meeting the requirements and your secure design. Choose reliable and secure technologies. You can use and adapt existing open-source LMS frameworks or build a simple prototype from scratch. Ensure you understand and configure reused components correctly to meet security requirements.

### Analysis

Validate your implementation against the design and security requirements. Describe your security analysis methodology, including any existing framework analyses and additional analyses. Refer to the OWASP Web Security Testing Guide and use advanced security analysis tools and techniques from practical labs. Include:

- Security guarantees of programming languages.
- Secure software design patterns.
- Security analysis of dependencies/libraries.
- Mitigations for common vulnerabilities.
- Security testing methodologies.
- Integrated source code analysis tools.
