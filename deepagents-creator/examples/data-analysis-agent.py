#!/usr/bin/env python3
"""
Data Analysis Agent Example

A DeepAgent specialized in loading, exploring, and analyzing datasets
with visualization and insight generation.
"""

import os
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langchain_core.tools import tool
import pandas as pd
import json


@tool
def load_dataset(filepath: str) -> str:
    """Load a dataset and return basic information."""
    try:
        # Determine file type and load
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(filepath)
        elif filepath.endswith('.json'):
            df = pd.read_json(filepath)
        else:
            return f"Unsupported file type: {filepath}"
        
        # Store globally for other operations
        global CURRENT_DATASET
        CURRENT_DATASET = df
        
        # Return dataset info
        info = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "missing_values": df.isnull().sum().to_dict(),
            "sample_rows": df.head(3).to_dict(orient='records')
        }
        
        return json.dumps(info, indent=2)
    
    except Exception as e:
        return f"Error loading dataset: {e}"


@tool
def analyze_column(column_name: str) -> str:
    """Analyze a specific column in the dataset."""
    try:
        if 'CURRENT_DATASET' not in globals():
            return "No dataset loaded. Use load_dataset first."
        
        df = CURRENT_DATASET
        
        if column_name not in df.columns:
            return f"Column '{column_name}' not found in dataset"
        
        col = df[column_name]
        
        analysis = {
            "column": column_name,
            "dtype": str(col.dtype),
            "count": len(col),
            "missing": col.isnull().sum(),
            "unique_values": col.nunique()
        }
        
        # Numeric column stats
        if pd.api.types.is_numeric_dtype(col):
            analysis.update({
                "mean": float(col.mean()),
                "median": float(col.median()),
                "std": float(col.std()),
                "min": float(col.min()),
                "max": float(col.max()),
                "quartiles": {
                    "25%": float(col.quantile(0.25)),
                    "50%": float(col.quantile(0.50)),
                    "75%": float(col.quantile(0.75))
                }
            })
        
        # Categorical column stats
        else:
            value_counts = col.value_counts().head(10)
            analysis["top_values"] = value_counts.to_dict()
        
        return json.dumps(analysis, indent=2)
    
    except Exception as e:
        return f"Error analyzing column: {e}"


@tool
def create_visualization(viz_type: str, columns: str, output_file: str) -> str:
    """Create a visualization and save to file."""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        if 'CURRENT_DATASET' not in globals():
            return "No dataset loaded. Use load_dataset first."
        
        df = CURRENT_DATASET
        columns_list = [c.strip() for c in columns.split(',')]
        
        plt.figure(figsize=(10, 6))
        
        if viz_type == "histogram":
            df[columns_list[0]].hist(bins=30)
            plt.xlabel(columns_list[0])
            plt.ylabel("Frequency")
            plt.title(f"Distribution of {columns_list[0]}")
        
        elif viz_type == "scatter":
            plt.scatter(df[columns_list[0]], df[columns_list[1]], alpha=0.5)
            plt.xlabel(columns_list[0])
            plt.ylabel(columns_list[1])
            plt.title(f"{columns_list[0]} vs {columns_list[1]}")
        
        elif viz_type == "boxplot":
            df[columns_list].boxplot()
            plt.ylabel("Values")
            plt.title("Box Plot")
        
        elif viz_type == "correlation":
            sns.heatmap(df[columns_list].corr(), annot=True, cmap='coolwarm')
            plt.title("Correlation Matrix")
        
        else:
            return f"Unknown visualization type: {viz_type}"
        
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        
        return f"Visualization saved to {output_file}"
    
    except Exception as e:
        return f"Error creating visualization: {e}"


@tool
def run_statistical_test(test_type: str, columns: str) -> str:
    """Run statistical tests on data."""
    try:
        from scipy import stats
        
        if 'CURRENT_DATASET' not in globals():
            return "No dataset loaded. Use load_dataset first."
        
        df = CURRENT_DATASET
        columns_list = [c.strip() for c in columns.split(',')]
        
        if test_type == "correlation":
            corr, p_value = stats.pearsonr(df[columns_list[0]], df[columns_list[1]])
            return json.dumps({
                "test": "Pearson Correlation",
                "correlation": float(corr),
                "p_value": float(p_value),
                "significant": p_value < 0.05
            }, indent=2)
        
        elif test_type == "ttest":
            group1 = df[df[columns_list[0]] == df[columns_list[0]].unique()[0]][columns_list[1]]
            group2 = df[df[columns_list[0]] == df[columns_list[0]].unique()[1]][columns_list[1]]
            t_stat, p_value = stats.ttest_ind(group1, group2)
            return json.dumps({
                "test": "T-Test",
                "t_statistic": float(t_stat),
                "p_value": float(p_value),
                "significant": p_value < 0.05
            }, indent=2)
        
        elif test_type == "normality":
            stat, p_value = stats.shapiro(df[columns_list[0]].dropna())
            return json.dumps({
                "test": "Shapiro-Wilk Normality Test",
                "statistic": float(stat),
                "p_value": float(p_value),
                "normal": p_value > 0.05
            }, indent=2)
        
        else:
            return f"Unknown test type: {test_type}"
    
    except Exception as e:
        return f"Error running statistical test: {e}"


def create_data_analyst():
    """Create a data analysis agent."""
    
    # Hybrid backend
    backend = CompositeBackend(
        default=StateBackend(),
        routes={
            "/analysis/": StoreBackend(),  # Persistent analysis results
            "/visualizations/": StateBackend()  # Temp visualizations
        }
    )
    
    system_prompt = """
    You are a professional data analyst specializing in exploratory data analysis.
    
    Analysis Workflow:
    1. **Load Data**: Use load_dataset to load the dataset
    2. **Explore Structure**:
       - Examine columns and data types
       - Check for missing values
       - Understand data distribution
    3. **Analyze Columns**:
       - Use analyze_column for key variables
       - Identify patterns and anomalies
       - Check distributions
    4. **Statistical Analysis**:
       - Calculate correlations
       - Run appropriate statistical tests
       - Validate assumptions
    5. **Visualize**:
       - Create relevant plots
       - Identify visual patterns
       - Support findings with charts
    6. **Generate Insights**:
       - Summarize key findings
       - Identify actionable insights
       - Note limitations and caveats
    7. **Save Results**: Store analysis in /analysis/
    
    Analysis Best Practices:
    - Always check for missing data first
    - Verify data types are correct
    - Look for outliers and anomalies
    - Test statistical assumptions
    - Use appropriate visualizations
    - Provide context for findings
    - Note confidence levels
    - Acknowledge limitations
    
    Visualization Guidelines:
    - histogram: For single variable distributions
    - scatter: For relationships between two variables
    - boxplot: For comparing distributions
    - correlation: For multiple variable relationships
    
    Statistical Tests:
    - correlation: Relationship between two continuous variables
    - ttest: Difference between two groups
    - normality: Test if data is normally distributed
    
    Report Structure:
    # Data Analysis Report
    
    ## Dataset Overview
    [Rows, columns, data types]
    
    ## Data Quality
    [Missing values, outliers, issues]
    
    ## Key Findings
    1. [Finding with statistical support]
    2. [Finding with visualization]
    ...
    
    ## Statistical Analysis
    [Detailed statistical results]
    
    ## Visualizations
    [List of created visualizations]
    
    ## Insights & Recommendations
    [Actionable insights]
    
    ## Limitations
    [Data quality issues, caveats]
    """
    
    agent = create_deep_agent(
        model="anthropic:claude-sonnet-4-20250514",
        tools=[load_dataset, analyze_column, create_visualization, run_statistical_test],
        backend=backend,
        system_prompt=system_prompt
    )
    
    return agent


def analyze_dataset(agent, filepath: str):
    """Run complete analysis on a dataset."""
    print(f"\n{'='*60}")
    print(f"Analyzing: {filepath}")
    print(f"{'='*60}\n")
    
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"""
            Perform a comprehensive analysis of the dataset: {filepath}
            
            Tasks:
            1. Load and explore the dataset
            2. Analyze key variables
            3. Create relevant visualizations
            4. Run statistical tests
            5. Generate insights report
            6. Save results to /analysis/
            """
        }]
    })
    
    print("\n" + "="*60)
    print("Analysis Complete")
    print("="*60 + "\n")
    print(result["messages"][-1].content)
    
    return result


def main():
    """Main execution."""
    # Create data analyst
    agent = create_data_analyst()
    
    # Example: Analyze a dataset
    # Replace with your actual dataset path
    dataset_path = "data/sample_data.csv"
    
    # For testing, create sample data
    import pandas as pd
    import numpy as np
    
    os.makedirs("data", exist_ok=True)
    
    # Create sample dataset
    np.random.seed(42)
    df = pd.DataFrame({
        'age': np.random.randint(18, 80, 1000),
        'income': np.random.normal(50000, 15000, 1000),
        'score': np.random.normal(75, 10, 1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000),
        'satisfied': np.random.choice([True, False], 1000)
    })
    df.to_csv(dataset_path, index=False)
    
    # Run analysis
    result = analyze_dataset(agent, dataset_path)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    main()
