# Work Impact Analyzer

A powerful AI-driven tool that analyzes your work documents and provides intelligent insights based on your questions.

## 🚀 Features

- **Document Analysis**: Automatically reads and processes Microsoft Word (.docx) files
- **Natural Language Queries**: Ask questions about your work in plain English  
- **Multiple Interfaces**: Choose from simple UI, advanced UI, or command-line options
- **AI-Powered Insights**: Get leadership summaries, performance reviews, and skill analysis
- **Progress Tracking**: Real-time feedback during document processing

## 📁 Setup

### 1. Prerequisites

Make sure you have Python 3.8+ installed with the required packages:

```powershell
pip install gradio python-docx openai
```

### 2. Document Preparation

1. Create a `work_doc` folder in the project directory
2. Add your Microsoft Word (.docx) files to this folder
3. The tool will automatically detect and process all .docx files

### 3. Configuration

Ensure your LLM client is properly configured in `llm_client.py` with your API credentials.

## 🎯 Usage

### Option 1: Interactive Launcher (Recommended)

Run the launcher script to choose your preferred interface:

```powershell
python launcher.py
```

This will show you a menu with the following options:
- **Simple UI**: Basic web interface with essential features
- **Advanced UI**: Enhanced web interface with multiple tabs and features  
- **Command Line**: Direct analysis from the terminal
- **Exit**: Close the application

### Option 2: Direct Interface Launch

#### Simple Web UI
```powershell
python gradio_ui.py
```

#### Advanced Web UI  
```powershell
python gradio_advanced_ui.py
```

#### Command Line
```powershell
python work_impact_agent.py "Your question here"
```

## 💡 Example Questions

Here are some effective prompts to get you started:

### Leadership & Performance
- "Please provide a leadership summary of my work"
- "What are my key achievements and impact?"
- "Create a performance review summary based on my work"

### Skills & Expertise
- "What skills and expertise do I demonstrate in my work?"
- "What are my technical competencies based on these documents?"
- "How do I show leadership and collaboration skills?"

### Project Analysis
- "Summarize my contributions to different projects"
- "What are the main themes and focus areas in my work?"
- "How do my projects show business impact?"

### Career Development
- "What growth opportunities are evident in my work?"
- "How has my work evolved over time?"
- "What are my strongest professional accomplishments?"

## 🖥️ Interface Guide

### Simple UI Features
- Clean, straightforward interface
- Basic document analysis
- Copy results functionality
- Example prompts for guidance

### Advanced UI Features
- **Multiple Tabs**: Separate sections for analysis, instructions, and about info
- **File Status Monitoring**: Real-time view of documents in your work_doc folder
- **Progress Tracking**: Visual feedback during processing
- **Enhanced Styling**: Professional appearance with custom CSS
- **Comprehensive Help**: Built-in documentation and tips

### Command Line Features
- Direct terminal execution
- Scriptable for automation
- Minimal interface for quick analysis
- Perfect for integration with other tools

## 📊 Document Requirements

### Supported Formats
- Microsoft Word (.docx) files only
- Multiple files processed simultaneously
- Automatic text extraction from paragraphs

### File Organization
```
WorkSummaryBot/
├── work_doc/              # Place your .docx files here
│   ├── March_2025.docx
│   ├── April_2025.docx
│   └── May_2025.docx
├── gradio_ui.py          # Simple web interface
├── gradio_advanced_ui.py # Advanced web interface  
├── launcher.py           # Interactive launcher
└── work_impact_agent.py  # Core analysis engine
```

## 🔧 Troubleshooting

### Common Issues

**"No documents found"**
- Ensure .docx files are in the `work_doc` folder
- Check that files aren't corrupted or password-protected
- Verify file extensions are exactly `.docx`

**"Module not found" errors**  
- Install missing packages: `pip install gradio python-docx openai`
- Ensure you're using the correct Python environment

**"LLM connection failed"**
- Check your API credentials in `llm_client.py`
- Verify your internet connection
- Ensure your LLM service is accessible

**Interface won't start**
- Try a different port if 7860 is occupied
- Check firewall settings
- Restart the terminal and try again

### Getting Help

1. **Check Logs**: The application provides detailed logging information
2. **File Status**: Use the "Refresh File List" button to check document detection
3. **Example Prompts**: Start with provided examples to test functionality

## 🔒 Privacy & Security

- Documents are processed according to your LLM configuration
- No permanent storage of document content by the interface
- All processing happens in real-time
- Ensure your LLM API settings meet your privacy requirements

## 🆕 Updates & Versions

### Version 1.0.0
- Initial release with basic functionality
- Support for .docx document processing
- Multiple interface options
- AI-powered analysis capabilities

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the logs for detailed error messages  
3. Verify your setup follows the requirements

---

**Created with ❤️ for productivity and professional development**