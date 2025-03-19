# test_integration.py
import os
from app import create_app
from app.services.document_parser import extract_text_from_document
from app.services.ai_processor import process_project_overview
from app.services.ms_project import create_project_schedule

def test_end_to_end():
    """Test the entire integration flow with a sample document"""
    # Create test document
    test_doc = "test_project.txt"
    with open(test_doc, "w") as f:
        f.write("""
        Project: AI Website Development
        
        We need to build an AI-powered website that integrates with Microsoft Project Professional.
        The site will allow users to upload project overviews and automatically generate project schedules.
        
        Key requirements:
        - Web interface for document upload
        - AI processing of project documents
        - Integration with Microsoft Project
        - Task management and resource allocation
        
        Team members:
        - Project Manager
        - Backend Developer 
        - Frontend Developer
        - AI Specialist
        - QA Engineer
        
        Timeline: The project should be completed within 2 months.
        """)
    
    try:
        # Extract text from document
        document_text = extract_text_from_document(test_doc)
        print("Text extraction successful.")
        
        # Process with AI
        project_data = process_project_overview(document_text)
        print("AI processing successful.")
        print(f"Detected {len(project_data['tasks'])} tasks and {len(project_data['resources'])} resources.")
        
        # Generate MS Project file
        project_file = create_project_schedule(project_data, "Test Project")
        print(f"Project file generation successful: {project_file}")
        
        print("End-to-end test completed successfully!")
        
    finally:
        # Clean up
        if os.path.exists(test_doc):
            os.remove(test_doc)

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        test_end_to_end()