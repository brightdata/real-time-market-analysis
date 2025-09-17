#!/usr/bin/env python3
"""
React Jobs Analysis Script
Analyzes remote React job data from CSV file to extract:
- Average salary information
- Most common skill requirements
- Job distribution by type and location
"""

import pandas as pd
import numpy as np
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Optional

class ReactJobsAnalyzer:
    def __init__(self, csv_path: str):
        """Initialize the analyzer with CSV data."""
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and clean the CSV data."""
        try:
            self.df = pd.read_csv(self.csv_path)
            print(f"Loaded {len(self.df)} job records")
            print(f"Columns: {list(self.df.columns)}")
        except FileNotFoundError:
            print(f"Error: Could not find file {self.csv_path}")
            return
        except Exception as e:
            print(f"Error loading data: {e}")
            return
    
    def parse_salary(self, salary_str: str) -> Tuple[Optional[float], Optional[float], str]:
        """
        Parse salary string and return (min_salary, max_salary, period).
        Returns None values if salary cannot be parsed.
        """
        if pd.isna(salary_str) or salary_str == "Not specified":
            return None, None, "unknown"
        
        # Remove currency symbols and clean the string
        clean_salary = re.sub(r'[$,]', '', str(salary_str))
        
        # Determine period (hourly, monthly, yearly)
        period = "yearly"
        if "/hour" in salary_str:
            period = "hourly"
        elif "/month" in salary_str:
            period = "monthly"
        elif "/week" in salary_str:
            period = "weekly"
        
        # Extract numeric ranges
        range_match = re.search(r'(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)', clean_salary)
        if range_match:
            min_sal = float(range_match.group(1))
            max_sal = float(range_match.group(2))
            return min_sal, max_sal, period
        
        # Extract single values with + indicator
        plus_match = re.search(r'(\d+(?:\.\d+)?)\+', clean_salary)
        if plus_match:
            min_sal = float(plus_match.group(1))
            return min_sal, None, period
        
        # Extract single numeric value
        single_match = re.search(r'(\d+(?:\.\d+)?)', clean_salary)
        if single_match:
            salary = float(single_match.group(1))
            return salary, salary, period
        
        return None, None, "unknown"
    
    def normalize_to_yearly(self, salary: float, period: str) -> float:
        """Convert salary to yearly equivalent."""
        if salary is None:
            return None
        
        multipliers = {
            "hourly": 2080,  # 40 hours/week * 52 weeks
            "weekly": 52,
            "monthly": 12,
            "yearly": 1
        }
        
        return salary * multipliers.get(period, 1)
    
    def analyze_salaries(self) -> Dict:
        """Analyze salary data and return statistics."""
        if self.df is None:
            return {}
        
        salary_data = []
        
        for _, row in self.df.iterrows():
            min_sal, max_sal, period = self.parse_salary(row['Salary Range'])
            
            if min_sal is not None:
                yearly_min = self.normalize_to_yearly(min_sal, period)
                yearly_max = self.normalize_to_yearly(max_sal if max_sal else min_sal, period)
                
                salary_data.append({
                    'job_title': row['Job Title'],
                    'company': row['Company'],
                    'min_yearly': yearly_min,
                    'max_yearly': yearly_max,
                    'avg_yearly': (yearly_min + yearly_max) / 2,
                    'original_period': period,
                    'job_type': row['Job Type']
                })
        
        if not salary_data:
            return {"error": "No valid salary data found"}
        
        salary_df = pd.DataFrame(salary_data)
        
        return {
            "total_jobs_with_salary": len(salary_df),
            "avg_salary": salary_df['avg_yearly'].mean(),
            "median_salary": salary_df['avg_yearly'].median(),
            "min_salary": salary_df['min_yearly'].min(),
            "max_salary": salary_df['max_yearly'].max(),
            "salary_by_job_type": salary_df.groupby('job_type')['avg_yearly'].agg(['mean', 'median', 'count']).to_dict(),
            "top_paying_jobs": salary_df.nlargest(10, 'avg_yearly')[['job_title', 'company', 'avg_yearly']].to_dict('records')
        }
    
    def extract_skills(self, skills_str: str) -> List[str]:
        """Extract individual skills from the skills string."""
        if pd.isna(skills_str):
            return []
        
        # Split by common delimiters and clean
        skills = re.split(r'[,;]', str(skills_str))
        cleaned_skills = []
        
        for skill in skills:
            # Clean and normalize skill names
            clean_skill = skill.strip().lower()
            clean_skill = re.sub(r'[^\w\s+#.]', '', clean_skill)
            
            if clean_skill and len(clean_skill) > 1:
                # Normalize common variations
                skill_mappings = {
                    'reactjs': 'react',
                    'react js': 'react',
                    'react.js': 'react',
                    'javascript': 'javascript',
                    'js': 'javascript',
                    'typescript': 'typescript',
                    'ts': 'typescript',
                    'nodejs': 'node.js',
                    'node js': 'node.js',
                    'nextjs': 'next.js',
                    'next js': 'next.js',
                    'react native': 'react native',
                    'html5': 'html',
                    'css3': 'css'
                }
                
                normalized_skill = skill_mappings.get(clean_skill, clean_skill)
                cleaned_skills.append(normalized_skill)
        
        return cleaned_skills
    
    def analyze_skills(self) -> Dict:
        """Analyze skill requirements and return statistics."""
        if self.df is None:
            return {}
        
        all_skills = []
        skill_combinations = []
        
        for _, row in self.df.iterrows():
            skills = self.extract_skills(row['Required Skills'])
            all_skills.extend(skills)
            if skills:
                skill_combinations.append(skills)
        
        skill_counter = Counter(all_skills)
        
        # Find common skill combinations
        combo_counter = Counter()
        for skills in skill_combinations:
            if len(skills) >= 2:
                # Sort skills to normalize combinations
                sorted_skills = tuple(sorted(skills))
                combo_counter[sorted_skills] += 1
        
        return {
            "total_skills_mentioned": len(all_skills),
            "unique_skills": len(skill_counter),
            "most_common_skills": skill_counter.most_common(20),
            "skill_frequency_percent": {skill: (count/len(skill_combinations))*100 
                                     for skill, count in skill_counter.most_common(15)},
            "common_skill_combinations": combo_counter.most_common(10)
        }
    
    def analyze_job_distribution(self) -> Dict:
        """Analyze job distribution by various factors."""
        if self.df is None:
            return {}
        
        return {
            "job_type_distribution": self.df['Job Type'].value_counts().to_dict(),
            "location_distribution": self.df['Location'].value_counts().to_dict(),
            "source_distribution": self.df['Source'].value_counts().to_dict(),
            "companies_with_most_jobs": self.df['Company'].value_counts().head(10).to_dict()
        }
    
    def generate_visualizations(self):
        """Generate and save visualization plots."""
        if self.df is None:
            return
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Remote React Jobs Analysis', fontsize=16, fontweight='bold')
        
        # 1. Job Type Distribution
        job_types = self.df['Job Type'].value_counts()
        axes[0, 0].pie(job_types.values, labels=job_types.index, autopct='%1.1f%%')
        axes[0, 0].set_title('Job Type Distribution')
        
        # 2. Top Skills
        skills_analysis = self.analyze_skills()
        if 'most_common_skills' in skills_analysis:
            top_skills = skills_analysis['most_common_skills'][:10]
            skills, counts = zip(*top_skills)
            axes[0, 1].barh(skills, counts)
            axes[0, 1].set_title('Top 10 Required Skills')
            axes[0, 1].set_xlabel('Frequency')
        
        # 3. Source Distribution
        sources = self.df['Source'].value_counts()
        axes[1, 0].bar(sources.index, sources.values)
        axes[1, 0].set_title('Jobs by Source')
        axes[1, 0].set_xlabel('Job Source')
        axes[1, 0].set_ylabel('Number of Jobs')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. Salary Distribution (if available)
        salary_analysis = self.analyze_salaries()
        if 'error' not in salary_analysis:
            # Create salary ranges for histogram
            salary_data = []
            for _, row in self.df.iterrows():
                min_sal, max_sal, period = self.parse_salary(row['Salary Range'])
                if min_sal:
                    yearly_avg = self.normalize_to_yearly((min_sal + (max_sal or min_sal))/2, period)
                    if yearly_avg and yearly_avg < 1000000:  # Filter outliers
                        salary_data.append(yearly_avg)
            
            if salary_data:
                axes[1, 1].hist(salary_data, bins=15, edgecolor='black', alpha=0.7)
                axes[1, 1].set_title('Salary Distribution (Yearly)')
                axes[1, 1].set_xlabel('Salary ($)')
                axes[1, 1].set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('react_jobs_analysis.png', dpi=300, bbox_inches='tight')
        print("Visualization saved as 'react_jobs_analysis.png'")
    
    def generate_report(self) -> str:
        """Generate a comprehensive text report."""
        if self.df is None:
            return "Error: No data loaded"
        
        salary_analysis = self.analyze_salaries()
        skills_analysis = self.analyze_skills()
        distribution_analysis = self.analyze_job_distribution()
        
        report = []
        report.append("=" * 60)
        report.append("REMOTE REACT JOBS ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Total Jobs Analyzed: {len(self.df)}")
        report.append("")
        
        # Salary Analysis
        report.append("SALARY ANALYSIS")
        report.append("-" * 20)
        if 'error' not in salary_analysis:
            report.append(f"Jobs with salary info: {salary_analysis['total_jobs_with_salary']}")
            report.append(f"Average salary: ${salary_analysis['avg_salary']:,.0f}")
            report.append(f"Median salary: ${salary_analysis['median_salary']:,.0f}")
            report.append(f"Salary range: ${salary_analysis['min_salary']:,.0f} - ${salary_analysis['max_salary']:,.0f}")
            report.append("")
            
            report.append("Top 5 Highest Paying Jobs:")
            for i, job in enumerate(salary_analysis['top_paying_jobs'][:5], 1):
                report.append(f"{i}. {job['job_title']} at {job['company']} - ${job['avg_yearly']:,.0f}")
        else:
            report.append("No valid salary data found")
        report.append("")
        
        # Skills Analysis
        report.append("SKILLS ANALYSIS")
        report.append("-" * 20)
        report.append(f"Total skills mentioned: {skills_analysis['total_skills_mentioned']}")
        report.append(f"Unique skills: {skills_analysis['unique_skills']}")
        report.append("")
        
        report.append("Top 15 Most Required Skills:")
        for i, (skill, count) in enumerate(skills_analysis['most_common_skills'][:15], 1):
            percentage = skills_analysis['skill_frequency_percent'].get(skill, 0)
            report.append(f"{i:2d}. {skill.title():<20} - {count:3d} jobs ({percentage:.1f}%)")
        report.append("")
        
        # Job Distribution
        report.append("JOB DISTRIBUTION")
        report.append("-" * 20)
        
        report.append("By Job Type:")
        for job_type, count in distribution_analysis['job_type_distribution'].items():
            percentage = (count / len(self.df)) * 100
            report.append(f"  {job_type}: {count} ({percentage:.1f}%)")
        report.append("")
        
        report.append("By Source:")
        for source, count in distribution_analysis['source_distribution'].items():
            percentage = (count / len(self.df)) * 100
            report.append(f"  {source}: {count} ({percentage:.1f}%)")
        report.append("")
        
        report.append("Companies with Most Job Postings:")
        for i, (company, count) in enumerate(list(distribution_analysis['companies_with_most_jobs'].items())[:10], 1):
            report.append(f"{i:2d}. {company}: {count} jobs")
        
        return "\n".join(report)

def main():
    """Main function to run the analysis."""
    csv_path = r"d:\Triallies\BrightKiro\remote_react_jobs.csv"
    
    print("Starting React Jobs Analysis...")
    analyzer = ReactJobsAnalyzer(csv_path)
    
    if analyzer.df is None:
        print("Failed to load data. Exiting.")
        return
    
    # Generate comprehensive report
    report = analyzer.generate_report()
    print(report)
    
    # Save report to file
    with open('react_jobs_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nDetailed report saved to 'react_jobs_analysis_report.txt'")
    
    # Generate visualizations
    try:
        analyzer.generate_visualizations()
    except Exception as e:
        print(f"Could not generate visualizations: {e}")
        print("Make sure matplotlib and seaborn are installed: pip install matplotlib seaborn")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()