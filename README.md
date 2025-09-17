<p align="center">
  <a href="https://brightdata.com/">
    <img src="https://mintlify.s3.us-west-1.amazonaws.com/brightdata/logo/light.svg" width="300" alt="Bright Data Logo">
  </a>
</p>

# Kiro + Bright Data MCP: Agentic Real-Time Market Analysis

Seamlessly connect Kiro’s AI agentic IDE to Bright Data’s Web MCP server.
Transform static prompts into live web scraping, automated data processing, and instant reporting—without manual scraping code or fiddly data wrangling!

<div align="center">
  <img src="https://img.shields.io/badge/python-3.9+-blue"/>
  <img src="https://img.shields.io/badge/Node.js-18+-success"/>
  <img src="https://img.shields.io/badge/Kiro-Agentic-blueviolet"/>
  <img src="https://img.shields.io/badge/License-MIT-blue"/>
</div>

---

## Features 🚀

- AI-powered, spec-driven automation: [Kiro](https://kiro.dev/) converts natural language into multi-step data workflows.
- Live web powered: [Bright Data's Web MCP](https://github.com/brightdata/brightdata-mcp) adds live search, scraping, and data structuring tools—CAPTCHAs and anti-bots are solved for you.
- No glue code required: Scrape, parse, save as CSV, and generate a Python analysis pipeline—100% automated.
- Robust and adaptive: Bulk and fallback scraping, auto-handling timeouts and bot protection.
- Ready-to-use insights: Generates reports, charts, and stats for direct business/research use.

---

## End-to-End Example: "Remote React Developer Jobs" Market Research

Prompt in Kiro:
```
    Search for "remote React developer jobs" on Google,
    scrape the top 5 job listing websites, extract job titles, companies,
    salary ranges, and required skills.
    Create a CSV with this data and generate a Python script that analyzes
    average salaries and most common requirements.
```
Kiro’s Steps:

- Uses ```search_engine``` to get live job-board links.
- Bulk scrapes (falls back to single-site scraping as needed).
- Auto-parses to ```remote_react_jobs.csv```.
- Generates ```analyze_react_jobs.py```—a complete analytics script.
- Produces ```react_jobs_analysis_report.txt``` (summary) and ```react_jobs_analysis.png``` (visual insights).

Result:
Structured, analysis-ready, live labor market data for React remote jobs, including titles, employers, salaries, locations, skills, and job-board source.

---

## What’s in This Repository? 📦
```
| File                         | Purpose                                                      |
|------------------------------|--------------------------------------------------------------|
| remote_react_jobs.csv        | Live-scraped job listings (all fields structured)            |
| analyze_react_jobs.py        | Automated data analysis and report generator                 |
| requirements.txt             | Python dependencies (pandas, numpy, matplotlib, seaborn)     |
| react_jobs_analysis_report.txt | Human-readable summary stats and skill trends             |
| react_jobs_analysis.png      | Salary, skill, source, and job-type visualizations           |
```
---

## How It Works

1. Kiro interprets your intent and plans a workflow, leveraging MCP tools to fetch and process live data.
2. Bright Data’s MCP server provides:
    - ```search_engine```: Fresh Google/Bing/Yandex SERPs.
    - ```scrape_as_markdown```: Clean markdown conversion.
    - ```scrape_batch```: Bulk, adaptive page scraping.
    - ```web_data_amazon_product```: Structured Amazon product data (for other scenarios!).
3. Automated extraction, data cleaning, CSV save, and Python analytic script generation—all from a single prompt.

---

## Prerequisites 🛠️

- Node.js 18+ (for Kiro + MCP)
- Python 3.9+ (for analytics)
- Kiro IDE access: https://kiro.dev
- Bright Data account: https://brightdata.com

---

## Setup Tutorial: Kiro + Bright Data MCP

1. Install and Launch Kiro

    - Request access at https://kiro.dev and follow install instructions.
    - Start Kiro—complete the onboarding wizard.

2. Create a Bright Data Account

    - Go to https://brightdata.com and sign up.
    - In the sidebar, open the MCP section, then choose Self-hosted mode.

3. Copy Your MCP Server Config

    - Copy the config block shown in your Bright Data portal.
    - Paste only the JSON (not surrounded by code fences) if pasting into a UI.
    Example:
```
        {
          "mcpServers": {
            "Bright Data": {
              "command": "npx",
              "args": ["@brightdata/mcp"],
              "env": {
                "API_TOKEN": "<your_api_token_here>"
              }
            }
          }
        }
```
4. Add the MCP Server to Kiro

    - In Kiro, open any folder/project.
    - In the sidebar, find the Kiro section > MCP SERVERS.
    - Remove the “default” server, and paste your config in (as above).
    - Wait for status to turn Connected.

5. Test the Integration

    - Click on any MCP tool (e.g., search_engine) in Kiro.
    - You should see live results or a tool GUI in chat.

  **For the full tutorial, visit our blog 👉 [Kiro x Web MCP](https://brightdata.com/blog/ai/kiro-with-web-mcp)**

---

## Run Your First Automated Task

Prompt Example:
```
    Search for "remote React developer jobs" on Google, scrape the top 5 job listing websites, extract job titles, companies, salary ranges, and required skills. Create a CSV file with this data and generate a Python script that analyzes average salaries and most common requirements.
```
Kiro will:
- Call each MCP tool to fetch, scrape, and process job data
- Save as ```remote_react_jobs.csv```
- Generate ```analyze_react_jobs.py``` for analytics

Run Analysis Locally:
```
    pip install -r requirements.txt
    python analyze_react_jobs.py

Results:
- react_jobs_analysis_report.txt (text summary)
- react_jobs_analysis.png (charts/visualizations)
```
---

## Output Examples

**[remote_react_jobs.csv](https://github.com/brightdata/real-time-market-analysis/blob/main/remote_react_jobs.csv)**
```
    Job Title,Company,Salary Range,Location,Job Type,Required Skills,Source
    Backend Software Engineer - AI Trainer,DataAnnotation,$40+/hour,Remote,Contract,"JavaScript, TypeScript, Python, C, C#, C++, React, Go, Java, Kotlin, Swift",Indeed
    ...
```
**[react_jobs_analysis_report.txt](https://github.com/brightdata/real-time-market-analysis/blob/main/react_jobs_analysis_report.txt)**
```
    ============================================================
    REMOTE REACT JOBS ANALYSIS REPORT
    ============================================================
    Total Jobs Analyzed: 72
    SALARY ANALYSIS
    --------------------
    Jobs with salary info: 52
    Average salary: $116,954
    ...
```
**Sample Visualization**

  <img src="https://github.com/brightdata/real-time-market-analysis/blob/main/react_jobs_analysis.png"/>
  
---

## FAQ

Q: What if scrape_batch times out?
A: Kiro automatically retries one URL at a time—no data lost, minimal manual intervention.

Q: Is this only for jobs data?
A: No—use any prompt for pricing, product research, competitive analysis, or content aggregation. Just change your intent!

Q: Can I add more MCP tools?
A: Yes—Bright Data’s MCP is extensible for almost any public web data needs.

---

## Next Steps

- Explore Bright Data’s AI/MCP integrations: https://docs.brightdata.com/integrations/ai-integrations
- Try pre-collected datasets: https://brightdata.com/products/datasets
- Integrate with [CrewAI](https://brightdata.com/blog/ai/crewai-with-bright-data-mcp-web-scraping), [n8n](https://brightdata.com/ai/mcp-server/n8n), [LangChain](https://docs.brightdata.com/mcp-server/integrations/langchain), [LlamaIndex](https://brightdata.com/blog/ai/chatbot-with-llamaindex-and-bright-data), etc., for even more [agentic apps](https://brightdata.com/use-cases/apps-agents).
- Have questions? Bright Data support: https://brightdata.com/contact

---

<p align="center">
  <b>
    Speed up research and automation: let Kiro and Bright Data MCP do the searching, scraping, structuring, and reporting for you!
  </b>
</p>
