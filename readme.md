# Generate Test Report to GitHub Pages Action

This GitHub Action automates the process of generating and publishing test reports to your GitHub Pages site. By collecting your HTML test reports generated during CI/CD workflows, it creates a dashboard that allows easy viewing and tracking of test results over time.

## Purpose

The purpose of this action is to streamline the collection and publication of HTML test reports to GitHub Pages. It enables you to:

- Collect multiple HTML test reports from various stages of your CI/CD pipeline.
- Organize and store these reports in a structured manner on your GitHub Pages site.
- Generate a dynamic dashboard (`index.html`) that lists all test reports with relevant metadata such as report name, timestamp, commit SHA, and run number.
- Provide direct links to individual test reports from the dashboard for detailed analysis.

## Action Parameters

### Inputs

The action accepts the following inputs:

- **`report_name`** *(required)*:  
  Description: A descriptive name for the test report. This name will be displayed on the dashboard.  
  Example: `"Integration Test Report - Build #42"`

- **`report_directory_name`** *(required)*:  
  Description: The directory name where the report will be stored within the GitHub Pages site. This should be unique to avoid conflicts with existing reports.  
  Example: `"integration-test-report-42"`

- **`commit_sha`** *(optional, default: `${{ github.sha }}`)*:  
  Description: The commit SHA associated with the test report. Useful for tracking which version of the code the report corresponds to.  
  Example: `"a1b2c3d4"`

- **`run_number`** *(optional, default: `${{ github.run_number }}`)*:  
  Description: The GitHub Actions run number for the workflow. Helps associate the report with a specific workflow run.  
  Example: `"42"`

- **`gh_page_path`** *(required)*:  
  Description: The local directory path to your GitHub Pages site where reports will be generated. Typically, this is the path to your `gh-pages` branch.  
  Example: `"./gh-pages"`

### Environment Variables

In addition to inputs, the action uses environment variables to collect paths to your HTML test reports:

- **`TEST_REPORT_<REPORT_TYPE>_PATH`**:  
  Description: Environment variables following the pattern `TEST_REPORT_<REPORT_TYPE>_PATH` specify the paths to individual HTML test reports. The `<REPORT_TYPE>` serves as a label for each report.  
  Example:

  ```yaml
  env:
    TEST_REPORT_UNIT_PATH: "./test-results/unit/html"
    TEST_REPORT_E2E_PATH: "./test-results/e2e/html"
  ```

  In this example:
  - `unit` tests report is located at `./test-results/unit/html`.
  - `e2e` (end-to-end) tests report is located at `./test-results/e2e/html`.

**Note**: Only HTML reports are supported by this action.

## How to Use This Action

To use this action, follow these steps:

1. **Set Up GitHub Pages Branch**  
   Ensure you have a `gh-pages` branch in your repository configured for GitHub Pages. This action will publish reports to this branch.

2. **Include the Action in Your Workflow**  
   Add the action to your GitHub Actions workflow file. Include any necessary steps to generate your test reports before invoking this action.

3. **Provide Inputs and Environment Variables**  
   - Specify the required inputs (`report_name`, `report_directory_name`, and `gh_page_path`).
   - Set environment variables for each test report using the `TEST_REPORT_<REPORT_TYPE>_PATH` pattern.

4. **Configure Git Checkout for GitHub Pages**  
   - Use `actions/checkout` to check out the `gh-pages` branch where reports will be stored.
   - Ensure the `gh_pages` directory is correctly specified in `gh_page_path`.

5. **Commit and Push Reports**  
   After the action runs, commit and push the changes to the `gh-pages` branch to update your GitHub Pages site.

### Example Workflow

Here's an example of how to set up your workflow to use this action:

```yaml
name: CI and Report Publishing

on:
  push:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Set Up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Unit Tests
        run: |
          mkdir -p test-results/unit/html
          pytest tests/unit --html=test-results/unit/html/index.html --self-contained-html

      - name: Run Integration Tests
        run: |
          mkdir -p test-results/integration/html
          pytest tests/integration --html=test-results/integration/html/index.html --self-contained-html

      - name: Checkout gh-pages Branch
        uses: actions/checkout@v3
        with:
          ref: gh-pages
          path: gh-pages

      - name: Generate and Publish Test Reports
        uses: chalermporn17/gh-page-test-report@v0.1.1
        with:
          report_name: 'Automated Test Reports'
          report_directory_name: 'test-report-${{ github.run_number }}'
          gh_page_path: './gh-pages'
        env:
          TEST_REPORT_UNIT_PATH: './test-results/unit/html'
          TEST_REPORT_INTEGRATION_PATH: './test-results/integration/html'

      - name: Commit and Push Reports to gh-pages
        run: |
          cd gh-pages
          git config user.name 'github-actions[bot]'
          git config user.email 'github-actions[bot]@users.noreply.github.com'
          git add .
          git commit -m 'Add test reports for run ${{ github.run_number }}'
          git push origin gh-pages
```

### Steps Breakdown

- **Checkout Repository**: Checks out the main repository code.
- **Set Up Python**: Sets up Python 3.12 to run tests and scripts.
- **Install Dependencies**: Installs necessary Python dependencies.
- **Run Unit and Integration Tests**: Executes tests and outputs HTML reports to specified directories.
- **Checkout gh-pages Branch**: Checks out the `gh-pages` branch to the `gh-pages` directory.
- **Generate and Publish Test Reports**: Invokes the action to process and publish test reports.
- **Commit and Push Reports**: Commits the generated reports and dashboard to the `gh-pages` branch.

## Important Notes

- **HTML Reports Only**: This action only supports test reports in HTML format. Ensure your testing framework can output reports in this format.
- **Unique Report Directory Names**: Use unique `report_directory_name` values (e.g., include `${{ github.run_number }}`) to prevent overwriting existing reports.
- **GitHub Token Permissions**: Ensure the `GITHUB_TOKEN` used in the workflow has the necessary permissions to push to the `gh-pages` branch.
- **Environment Variable Naming**: Environment variables for report paths must follow the `TEST_REPORT_<REPORT_TYPE>_PATH` pattern.
- **Action Path**: When referencing the action in your workflow, adjust the `uses` path according to where the action is stored in your repository.

## Understanding the Generated Dashboard

The action generates an `index.html` dashboard within your GitHub Pages site, which includes:

- **Test Report Listings**: Displays all published test reports with their metadata.
- **Filtering**: Allows filtering reports by name using a search input.
- **Sorting**: Clickable table headers enable sorting reports by timestamp or run number.
- **Direct Links**: Provides links to each individual test report for detailed viewing.
  
The dashboard automatically updates whenever new reports are published through this action.

## Customization

- **Dashboard Appearance**: The `index.html` template can be customized. It is located in the action's resources and can be modified to suit your preferences.
- **Report Types**: The labels for report types are derived from the `<REPORT_TYPE>` in the environment variable `TEST_REPORT_<REPORT_TYPE>_PATH`. Name these meaningfully to reflect the nature of the tests.

## Troubleshooting

- **No Reports Displayed**: Verify that the test reports are correctly generated and that the environment variables point to the correct paths.
- **Overwriting Reports**: If reports are being overwritten, make sure `report_directory_name` is unique for each run.

## Limitations

- **Single Format Support**: Currently, only HTML reports are supported. Reports in other formats will not be processed.
- **Manual Github Page Deploy Required**: The action does not automate the github page deployment. You need to include steps in your workflow to deploy to github page.

## Contributing

Contributions are welcome! If you have suggestions for improvements or encounter any issues, please open an issue or submit a pull request.