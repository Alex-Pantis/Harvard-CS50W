
# CS50W - Lecture 7: Testing, CI/CD
## Documentation

This document covers the key concepts from Lecture 7 of CS50W: Testing and CI/CD.

---

## Table of Contents
- [Testing](#testing)
  - [Why Testing?](#why-testing)
  - [Types of Testing](#types-of-testing)
  - [Testing in Django](#testing-in-django)
  - [Assert Functions](#assert-functions)
- [CI/CD](#cicd)
  - [Continuous Integration (CI)](#continuous-integration-ci)
  - [Continuous Delivery/Deployment (CD)](#continuous-deliverydeployment-cd)
  - [GitHub Actions](#github-actions)
  - [Example Workflows](#example-workflows)

---

## Testing

### Why Testing?

Testing is essential for ensuring that your code works as expected and continues to work as you make changes. Benefits include:

- **Catch bugs early** before they reach production
- **Confidence in refactoring** - make changes without breaking functionality
- **Documentation** - tests show how code is meant to be used
- **Regression prevention** - ensure old bugs don't reappear
- **Code quality** - writing testable code leads to better design

---

### Types of Testing

**Unit Testing:**
- Tests individual components or functions in isolation
- Smallest unit of testing
- Fast to run and easy to debug
- Example: Testing a single function that adds two numbers

**Integration Testing:**
- Tests how different parts of the application work together
- Tests interactions between components
- Example: Testing if a view correctly retrieves data from the database

**Functional Testing:**
- Tests the application from the user's perspective
- Tests complete workflows and user interactions
- Often uses browser automation (Selenium)
- Example: Testing the complete user registration process

---

### Testing in Django

Django provides a built-in testing framework based on Python's `unittest` module.

**Basic Test Structure:**

```python
from django.test import TestCase, Client
from .models import Flight, Airport

class FlightTestCase(TestCase):
    def setUp(self):
        # Create test data
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")
        
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
    
    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 2)
    
    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2)
        self.assertTrue(f.is_valid_flight())
    
    def test_invalid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())
```

**Testing Views:**

```python
def test_index(self):
    c = Client()
    response = c.get("/flights/")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context["flights"].count(), 2)

def test_valid_flight_page(self):
    a1 = Airport.objects.get(code="AAA")
    f = Flight.objects.get(origin=a1, destination=a1)
    
    c = Client()
    response = c.get(f"/flights/{f.id}")
    self.assertEqual(response.status_code, 200)

def test_invalid_flight_page(self):
    max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]
    
    c = Client()
    response = c.get(f"/flights/{max_id + 1}")
    self.assertEqual(response.status_code, 404)
```

**Running Tests:**
```bash
python manage.py test
```

---

### Assert Functions

Common assertion methods used in Django testing:

- `assertEqual(a, b)` - Check if a == b
- `assertNotEqual(a, b)` - Check if a != b
- `assertTrue(x)` - Check if x is True
- `assertFalse(x)` - Check if x is False
- `assertIn(a, b)` - Check if a is in b
- `assertNotIn(a, b)` - Check if a is not in b
- `assertIsNone(x)` - Check if x is None
- `assertIsNotNone(x)` - Check if x is not None
- `assertGreater(a, b)` - Check if a > b
- `assertLess(a, b)` - Check if a < b
- `assertRaises(Exception)` - Check if an exception is raised

---

## CI/CD

### Continuous Integration (CI)

**What is CI?**

Continuous Integration is the practice of automatically integrating code changes from multiple developers into a shared repository frequently. Each integration is verified by automated builds and tests.

**Key Principles:**
- Developers commit code regularly (multiple times per day)
- Every commit triggers an automated build
- Automated tests run on every build
- Fast feedback if something breaks
- Issues are identified and fixed quickly

**Benefits:**
- Detect integration problems early
- Reduce integration conflicts
- Always have a working version of the code
- Improve code quality through automated testing
- Increase confidence in the codebase

**Workflow:**
1. Developer pushes code to repository (GitHub)
2. CI server detects the push
3. CI server pulls the latest code
4. CI server runs automated tests
5. Developer receives feedback (pass/fail)

---

### Continuous Delivery/Deployment (CD)

**Continuous Delivery:**
- Code is always kept in a deployable state
- Automated deployment pipeline prepares code for release
- Manual approval required before deploying to production
- Deployment can happen at any time with one click

**Continuous Deployment:**
- Every change that passes all tests is automatically deployed to production
- No manual intervention required
- Fully automated release process
- Fastest way to get features to users

**Benefits:**
- Faster time to market
- Reduced deployment risk
- More frequent releases
- Less manual work and human error
- Better reliability

---

### GitHub Actions

GitHub Actions is a CI/CD platform that allows you to automate workflows directly in your GitHub repository.

**Key Concepts:**

**Workflows:**
- Automated processes defined in YAML files
- Stored in `.github/workflows/` directory
- Triggered by events (push, pull request, schedule, etc.)

**Jobs:**
- A set of steps that execute on the same runner
- Can run in parallel or sequentially
- Each job runs in a fresh virtual environment

**Steps:**
- Individual tasks within a job
- Can run commands or use actions
- Execute sequentially

**Runners:**
- Servers that run your workflows
- GitHub provides hosted runners (Ubuntu, Windows, macOS)
- Can also use self-hosted runners

---

### Example Workflows

**Basic Testing Workflow:**

```yaml
name: Testing
on: push

jobs:
  test_project:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run Django unit tests
      run: |
        pip3 install --user django
        python3 manage.py test
```

**Explanation:**
- `name`: Name of the workflow
- `on: push`: Trigger on every push to the repository
- `runs-on: ubuntu-latest`: Use Ubuntu as the operating system
- `uses: actions/checkout@v2`: Action that checks out your repository
- `run`: Commands to execute

**Advanced Workflow with Multiple Python Versions:**

```yaml
name: Testing
on: [push, pull_request]

jobs:
  test_project:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test
```

**Workflow with Deployment:**

```yaml
name: Deploy to Production
on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run tests
      run: |
        pip install -r requirements.txt
        python manage.py test
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to server
      run: |
        echo "Deploying to production..."
        # Add deployment commands here
```

**Explanation:**
- Tests run first
- Deployment only happens if tests pass (`needs: test`)
- Only deploys when code is pushed to the `main` branch

---

## Best Practices

**Testing:**
- Write tests as you develop code (Test-Driven Development)
- Aim for high test coverage
- Keep tests fast and independent
- Test edge cases and error conditions
- Use descriptive test names

**CI/CD:**
- Run tests on every commit
- Keep builds fast (under 10 minutes if possible)
- Fix broken builds immediately
- Use the same environment for testing and production
- Monitor your CI/CD pipelines
- Start simple and add complexity gradually

---

## Common CI/CD Triggers

```yaml
# On every push
on: push

# On push to specific branches
on:
  push:
    branches:
      - main
      - develop

# On pull requests
on: pull_request

# On schedule (cron)
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

# Multiple events
on: [push, pull_request]

# Manual trigger
on: workflow_dispatch
```

---

## Viewing Results

After setting up GitHub Actions:

1. Go to your repository on GitHub
2. Click on the **Actions** tab
3. View workflow runs and their status
4. Click on a specific run to see detailed logs
5. See which tests passed or failed

Green checkmark ✅ = All tests passed
Red X ❌ = Tests failed

---

## Summary

**Testing** ensures your code works correctly and continues to work as you make changes. Django provides a comprehensive testing framework for unit, integration, and functional tests.

**CI/CD** automates the process of testing and deploying code. Continuous Integration runs tests automatically on every commit, while Continuous Delivery/Deployment automates the release process.

**GitHub Actions** makes it easy to set up CI/CD workflows directly in your repository with simple YAML configuration files.

Together, testing and CI/CD create a robust development workflow that catches bugs early, maintains code quality, and enables rapid, reliable deployments.

---

*CS50W - Lecture 7: Testing, CI/CD*