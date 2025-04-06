import streamlit as st
import requests
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Assessment Search Tool",
    page_icon="🔍",
    layout="wide"
)

# API URL - this should point to your FastAPI service
API_URL = "http://localhost:8000"

def query_assessments(query: str):
    """Call the FastAPI backend to query assessments using only query string"""
    
    # Create request body
    request_data = {
        "query": query,
    }
    
    try:
        response = requests.post(f"{API_URL}/query", json=request_data)
        response.raise_for_status()  # Raise exception for error status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error querying API: {str(e)}")
        return {"results": [], "total_results": 0, "metadata_extracted": {}}

# Page header
st.title("Assessment Search Tool")
st.markdown("Search for assessments with natural language queries")

# Main search area

query = st.text_input(
    "Enter your search query",
    placeholder="E.g., Python assessments for senior developers that take less than 60 minutes"
)



# Search button
search_clicked = st.button("Search", type="primary")

# Show example queries
with st.expander("Example queries"):
    st.markdown("""
    - Show me all Python assessments
    - Find JavaScript assessments for junior developers
    - Senior level Java assessments under 45 minutes
    - Entry level coding tests in any language
    - Assessments longer than 60 minutes for mid-level engineers
    """)

# Search results
if search_clicked and query:
    with st.spinner("Searching for assessments..."):
        # Call API
        response = query_assessments(query=query)
        
        # Show results count
        st.subheader(f"Found {response['total_results']} matching assessments")
        
        # Display results
        if response["results"]:
            for i, result in enumerate(response["results"]):
                with st.expander(f"{i+1}. {result['title']} ({result['duration_minutes']} min)", expanded=i==0):
                    st.markdown(f"**Description:** {result['description']}")
                    st.markdown(f"**URL:** [{result['url']}]({result['url']})")
                    st.markdown(f"**Job Levels:** {', '.join(result['job_levels'])}")
                    st.markdown(f"**Languages:** {', '.join(result['languages'])}")
            
            # Create a dataframe for download
            df = pd.DataFrame([
                {
                    "Title": r["title"],
                    "Description": r["description"],
                    "URL": r["url"],
                    "Job Levels": ", ".join(r["job_levels"]),
                    "Languages": ", ".join(r["languages"]),
                    "Duration (min)": r["duration_minutes"],
                    "Score": r["similarity_score"]
                } for r in response["results"]
            ])
            
            # Download button
            st.download_button(
                label="Download Results as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name="assessment_results.csv",
                mime="text/csv",
            )
        else:
            st.info("No matching assessments found. Try broadening your search.")
elif search_clicked:
    st.warning("Please enter a search query")

# Footer
st.markdown("---")
st.caption("Assessment Search Tool © 2025")