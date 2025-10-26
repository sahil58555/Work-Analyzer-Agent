import gradio as gr
import logging
from work_impact_agent import work_impact_agent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_chat_message(user_message, chat_history, progress=gr.Progress()):
    """
    Process chat message and update chat history using the new messages format.
    """
    try:
        if not user_message.strip():
            return chat_history, "", gr.update(visible=True)
        
        progress(0.1, desc="Processing your message...")
        
        # Add user message to chat history (new format)
        chat_history.append({"role": "user", "content": user_message})
        
        progress(0.3, desc="Reading documents...")
        progress(0.5, desc="Analyzing with AI...")
        
        # Call the work_impact_agent with the user's prompt
        logger.info(f"Processing user message: {user_message[:100]}...")
        response = work_impact_agent(user_prompt=user_message)
        
        progress(0.9, desc="Formatting response...")
        
        if response:
            logger.info("Successfully received response from work_impact_agent")
            # Add AI response to chat history
            chat_history.append({"role": "assistant", "content": response})
            progress(1.0, desc="Complete!")
        else:
            logger.warning("No response received from work_impact_agent")
            chat_history.append({"role": "assistant", "content": "Sorry, I couldn't process your request. Please check that you have .docx files in the work_doc directory and try again."})
        
        return chat_history, "", gr.update(visible=True)  # Return updated chat, clear input, show chatbox
    
    except Exception as e:
        error_msg = f"An error occurred while processing your request: {str(e)}"
        logger.error(error_msg)
        chat_history.append({"role": "assistant", "content": error_msg})
        return chat_history, "", gr.update(visible=True)

def create_advanced_interface():
    """Create an advanced Gradio interface with top nav, left sidebar, and chat interface."""
    
    with gr.Blocks(
        title="Work Impact Analyzer",
        theme=gr.themes.Soft(),
        css="""
        /* Top Navigation Bar */
        .top-nav {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 30%, #334155 70%, #475569 100%);
            color: white;
            padding: 20px 40px;
            margin: -16px -16px 24px -16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(15px);
            position: relative;
            border-radius: 20px;
        }
        
        .top-nav::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 51, 234, 0.1) 100%);
            pointer-events: none;
            border-radius: 20px;
        }
        
        .nav-title {
            font-size: 28px;
            font-weight: 800;
            margin: 0 0 4px 0;
            background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .nav-subtitle {
            font-size: 15px;
            opacity: 0.85;
            margin: 0;
            font-weight: 400;
            color: #cbd5e1;
        }
        
        .nav-status {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 13px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        /* Profile Section */
        .profile-section {
            display: flex;
            align-items: center;
            gap: 16px;
            background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
            padding: 12px 20px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.25);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }
        
        .profile-image {
            position: relative;
        }
        
        .profile-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 18px;
            color: white;
            border: 3px solid rgba(255,255,255,0.9);
            box-shadow: 0 6px 20px rgba(0,0,0,0.2), 0 2px 8px rgba(102, 126, 234, 0.3);
            position: relative;
        }
        

        
        .profile-info {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        
        .profile-name {
            font-size: 18px;
            font-weight: 700;
            color: white;
            margin: 0;
            line-height: 1.2;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        .profile-role {
            font-size: 14px;
            color: #e2e8f0;
            margin: 0;
            line-height: 1.2;
            font-weight: 500;
        }
        
        .profile-company {
            font-size: 13px;
            color: #cbd5e1;
            margin: 0;
            line-height: 1.2;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        /* Main Layout */
        .main-container {
            display: flex;
            height: calc(100vh - 160px);
            gap: 24px;
            min-height: calc(100vh - 160px);
            padding: 0 16px;
        }
        
        /* Global font styling */
        * {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        }
        
        /* Left Sidebar */
        .sidebar {
            width: 300px;
            background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08), 0 4px 10px rgba(0,0,0,0.03);
            height: calc(100vh - 160px);
            max-height: calc(100vh - 160px);
            overflow-y: auto;
            position: sticky;
            top: 20px;
        }
        
        .sidebar-title {
            font-size: 17px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        }
        
        .example-btn {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 15px;
            padding: 8px 12px;
            margin: 4px 0;
            text-align: left;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            font-size: 13px;
            line-height: 1.3;
            width: 100%;
            display: block;
            font-weight: 500;
            color: #334155;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        }
        
        .example-btn:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3), 0 4px 10px rgba(102, 126, 234, 0.2);
            border-radius: 15px;
        }
        
        /* Scrollbar styling for sidebar */
        .sidebar::-webkit-scrollbar {
            width: 6px;
        }
        
        .sidebar::-webkit-scrollbar-track {
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .sidebar::-webkit-scrollbar-thumb {
            background: #c1c1c1;
            border-radius: 10px;
        }
        
        .sidebar::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8;
            border-radius: 10px;
        }
        

        
        /* Chat Interface */
        .chat-container {
            flex: 1;
            background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 20px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08), 0 4px 10px rgba(0,0,0,0.03);
            display: flex;
            flex-direction: column;
            height: 100%;
            max-height: 100%;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            padding: 20px 24px;
            border-radius: 20px 20px 0 0;
            border-bottom: 1px solid #e2e8f0;
            flex-shrink: 0;
        }
        
        .chat-title {
            font-size: 20px;
            font-weight: 700;
            color: #1e293b;
            margin: 0 0 4px 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        }
        
        .chat-subtitle {
            color: #64748b;
            margin: 0;
            font-size: 14px;
            font-weight: 400;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        }
        
        .chat-body {
            flex: 1;
            display: flex;
            flex-direction: column;
            height: calc(100% - 80px);
            min-height: 0;
        }
        
        .input-section {
            display: flex !important;
            flex-direction: column !important;
            gap: 12px !important;
            padding: 20px 24px !important;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
            border-top: 1px solid #e2e8f0 !important;
            border-radius: 0 0 20px 20px !important;
            flex-shrink: 0 !important;
            margin-left: 15px;
            margin-top: 10px;
        }
        
        .input-section > * {
            margin: 0 !important;
        }
        
        .chat-messages-section {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            min-height: 0;
        }
        
        .chat-messages {
            height: calc(100vh - 350px) !important;
            min-height: 400px !important;
            max-height: calc(100vh - 350px) !important;
            border: none !important;
            background: linear-gradient(145deg, #ffffff 0%, #fefefe 100%) !important;
            overflow-y: auto !important;
            transition: all 0.3s ease-in-out !important;
            padding: 16px !important;
            border-radius: 15px !important;
            margin: 16px !important;
        }
        
        /* Chat container wrapper for relative positioning */
        .chat-container-wrapper {
            position: relative !important;
            height: 400px !important;
            border-radius: 15px !important;
        }
        
        /* Chat messages positioning */
        .chat-messages {
            position: relative !important;
            height: 100% !important;
            border-radius: 15px !important;
        }
        
        /* Processing overlay - positioned within chatbox only */
        #processing_overlay {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            z-index: 999 !important;
            pointer-events: none !important;
            border-radius: 15px !important;
        }
        
        .processing-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: none;
            margin: 0;
        }
        
        /* Blur effect for chat messages when processing */
        .chat-messages.processing {
            filter: blur(4px) !important;
            opacity: 0.3 !important;
            transition: all 0.3s ease !important;
        }
        
        /* Blur effect for entire interface when processing */
        .gradio-container.processing {
            pointer-events: none;
        }
        
        .gradio-container.processing > *:not(#processing_overlay) {
            filter: blur(2px);
            opacity: 0.6;
        }
        
        /* Spinner animation */
        .spinner {
            width: 60px;
            height: 60px;
            border: 6px solid rgba(102, 126, 234, 0.2);
            border-top: 6px solid #667eea;
            border-right: 6px solid #764ba2;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 25px;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
            background: white;
        }
        
        @keyframes spin {
            0% { 
                transform: rotate(0deg);
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
            }
            50% {
                box-shadow: 0 12px 25px rgba(102, 126, 234, 0.5);
                transform: rotate(180deg);
            }
            100% { 
                transform: rotate(360deg);
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
            }
        }
        
        .processing-text {
            font-size: 20px;
            color: #667eea;
            font-weight: 700;
            text-align: center;
            text-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
            background: white;
            padding: 8px 16px;
            border-radius: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        /* Button row container */
        .button-row {
            display: flex !important;
            gap: 10px !important;
            width: 100% !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 25px !important;
            padding: 10px 12px !important;
            background: linear-gradient(145deg, #ffffff 0%, #fefefe 100%) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
            margin: 0 !important;
            align-items: center !important;
            box-sizing: border-box !important;
        }
        
        .send-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border-radius: 18px !important;
            padding: 12px 20px !important;
            margin: 0 !important;
            flex: 1 !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2) !important;
            transition: all 0.3s ease !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        }
        
        .send-btn:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
            border-radius: 18px !important;
        }
        
        .clear-btn {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
            color: white !important;
            border-radius: 18px !important;
            padding: 12px 20px !important;
            margin: 0 !important;
            flex: 1 !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2) !important;
            transition: all 0.3s ease !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        }
        
        .clear-btn:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3) !important;
            border-radius: 18px !important;
        }
        
        .chat-input {
            border-radius: 25px !important;
            border: 2px solid #e2e8f0 !important;
            padding: 16px 20px !important;
            font-size: 15px !important;
            width: 100% !important;
            background: linear-gradient(145deg, #ffffff 0%, #fefefe 100%) !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            color: #1e293b !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
            transition: all 0.3s ease !important;
            box-sizing: border-box !important;
            margin: 0 !important;
        }
        
        /* Ensure Row container shows button */
        .gradio-row {
            display: flex !important;
            align-items: center !important;
            gap: 0 !important;
            padding: 0 !important;
            background: transparent !important;
            border: none !important;
            width: 100% !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            border-radius: 25px !important;
        }
        
        /* Target the specific textbox container */
        .gradio-textbox {
            width: 100% !important;
            margin: 0 !important;
            border-radius: 25px !important;
        }
        
        .gradio-textbox textarea {
            margin: 0 !important;
            border-radius: 25px !important;
        }
        
        .chat-input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15), 0 4px 12px rgba(0,0,0,0.08) !important;
            outline: none !important;
            border-radius: 25px !important;
        }
        
        .output-section {
            flex: 1;
            min-height: 300px;
            border-radius: 20px;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f8fafc;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #cbd5e1 0%, #94a3b8 100%);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
            border-radius: 10px;
        }
        
        /* Additional styling */
        .gradio-container {
            max-width: none !important;
            padding: 0 !important;
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 50%, #cbd5e1 100%) !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            min-height: 100vh !important;
            border-radius: 20px !important;
        }
        
        .block {
            border: none !important;
            box-shadow: none !important;
            border-radius: 20px !important;
        }
        
        /* Animate the analysis output */
        .analysis-output {
            animation: fadeIn 0.5s ease-in;
            border-radius: 15px;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Progress bar styling */
        .progress-bar {
            background: linear-gradient(90deg, #667eea, #764ba2) !important;
            border-radius: 10px !important;
        }
        
        /* Hide progress bar from appearing in chat messages area */
        .gradio-chatbot .progress {
            display: none !important;
        }
        
        /* Show progress bar only in the textbox input area */
        .gradio-textbox .progress {
            display: block !important;
            position: relative !important;
            margin-top: 5px !important;
            background: transparent !important;
            padding: 0 !important;
            border-radius: 10px !important;
            box-shadow: none !important;
        }
        
        /* Hide progress in other locations */
        .gradio-container > .progress {
            display: none !important;
        }
        
        /* Accordion styling */
        .accordion {
            margin: 10px 0;
            border-radius: 15px;
        }
        
        /* Additional styling */
        .gradio-container {
            max-width: none !important;
            padding: 0 !important;
        }
        
        /* Responsive design */
        @media (max-width: 1200px) {
            .main-container {
                flex-direction: column;
                height: auto;
                min-height: calc(100vh - 200px);
            }
            
            .sidebar {
                width: 100%;
                max-height: 200px;
                border-radius: 20px;
            }
            
            .chat-messages {
                height: calc(100vh - 450px) !important;
                min-height: 300px !important;
                border-radius: 15px !important;
            }
            
            .top-nav {
                flex-direction: column;
                text-align: center;
                gap: 10px;
                border-radius: 20px;
            }
        }
        
        @media (max-width: 768px) {
            .top-nav {
                padding: 15px;
                margin: -8px -8px 15px -8px;
                flex-direction: column;
                gap: 15px;
                border-radius: 20px;
            }
            
            .nav-title {
                font-size: 18px;
            }
            
            .profile-section {
                order: -1;
                justify-content: center;
                border-radius: 20px;
            }
            
            .profile-avatar {
                width: 40px;
                height: 40px;
                font-size: 14px;
            }
            
            .profile-name {
                font-size: 15px;
            }
            
            .profile-role {
                font-size: 12px;
            }
            
            .profile-company {
                font-size: 11px;
            }
            
            .chat-messages {
                height: calc(100vh - 400px) !important;
                min-height: 250px !important;
                border-radius: 15px !important;
            }
            
            .input-section {
                padding: 10px;
                border-radius: 0 0 20px 20px !important;
            }
            
            .chat-header {
                padding: 10px 15px;
                border-radius: 20px 20px 0 0;
            }
            
            .sidebar {
                border-radius: 20px;
            }
            
            .chat-container {
                border-radius: 20px;
            }
        }
        """
    ) as demo:
        
        # Top Navigation Bar
        gr.HTML("""
        <div class="top-nav">
            <div class="nav-left">
                <div class="nav-title">🚀 Work Impact Analyzer</div>
                <div class="nav-subtitle">AI-powered professional portfolio analysis and insights</div>
            </div>
            <div style="display: flex; align-items: center; gap: 24px;">
                <div class="profile-section">
                    <div class="profile-image">
                        <div class="profile-avatar">SS</div>
                    </div>
                    <div class="profile-info">
                        <div class="profile-name">Sahil Saxena</div>
                        <div class="profile-role">Software Engineer</div>
                        <div class="profile-company">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 2L2 7V10C2 16 6 20.5 12 22C18 20.5 22 16 22 10V7L12 2Z"/>
                            </svg>
                            Microsoft
                        </div>
                    </div>
                </div>
                <div class="nav-status">📊 Portfolio Ready</div>
            </div>
        </div>
        """)
        
        # Instructions/Help Section (collapsible)
        with gr.Accordion("📖 About Sahil's Work Portfolio", open=False):
            gr.Markdown("""
            ### 🚀 Discover Sahil's Professional Journey
            
            **1. Explore Achievements** 🏆
            - Comprehensive analysis of Sahil's work documents
            - Key accomplishments and milestone contributions
            - Leadership initiatives and project outcomes
            
            **2. Ask About Impact** 💭
            - Click example queries to explore different aspects
            - Ask specific questions about Sahil's contributions
            - Get detailed insights about skills and expertise
            
            **3. Get Professional Insights** 🔍
            - Performance summaries and achievements
            - Career progression and growth areas
            - Skills assessment and recommendations
            
            ### 💡 What You Can Discover
            - **Leadership Impact**: Sahil's management and leadership contributions
            - **Project Success**: Key projects and their business outcomes  
            - **Skills & Growth**: Technical expertise and professional development
            - **Career Highlights**: Major achievements and recognitions
            
            ### 📊 Analysis Features
            - **Comprehensive Review**: Complete work portfolio analysis
            - **Achievement Mapping**: Detailed breakdown of accomplishments
            - **Impact Assessment**: Business value and contribution metrics
            - **Growth Tracking**: Professional development and skill evolution
            """)
        
        gr.HTML('<div style="margin: 20px 0;"></div>')  # Spacer
        
        # Main layout with sidebar and chat
        with gr.Row():
            # Left Sidebar - Examples
            with gr.Column(scale=1, min_width=300, elem_classes=["sidebar"]):
                gr.HTML("""
                <div class="sidebar-title">
                    💡 Interview & Manager Queries
                </div>
                <div style="margin-bottom: 10px; padding: 8px 12px; background: rgba(102, 126, 234, 0.1); border-radius: 15px; font-size: 12px; color: #667eea;">
                    <strong>📋 Performance Review Questions</strong><br>
                    Click any question below to analyze Sahil's work
                </div>
                """)
                
                # Example buttons
                example_btns = []
                example_prompts = [
                    "📊 Provide a leadership summary of Sahil's work",
                    "🎯 What are Sahil's key achievements and impact?",
                    "📋 Summarize Sahil's contributions to projects",
                    "🔧 What skills and expertise does Sahil demonstrate?",
                    "⭐ Create Sahil's performance review summary",
                    "🆕 How many new features added in last three months?",
                    "📈 Analyze Sahil's work themes and focus areas",
                    "🚀 Highlight Sahil's most impactful contributions",
                    "💼 Extract Sahil's career development insights",
                    "🆕 How many PRs merged in October 2025?",
                    "🐛 How many bug fixes in month of September 2025?",
                    "📈 How many commits made in August 2025?",
                    "🔧 How many unit tests added this quarter?",
                    "⚡ How many performance improvements implemented?",
                    "🔄 How many process optimizations delivered in 2025?",
                    "📊 What's the total PR count for the year 2025?",
                    "🆕 What is Sahil's business impact and ROI?",
                    "👥 How does Sahil collaborate and lead teams?",
                    "🏆 What awards or recognitions has Sahil received?",
                    "📚 Show Sahil's learning and development activities",
                    "⚡ What innovations or improvements has Sahil driven?",
                    "🎖️ Demonstrate Sahil's problem-solving abilities",
                    "📊 What metrics show Sahil's performance excellence?",
                    "🌟 How has Sahil exceeded expectations?",
                    "🔄 Show Sahil's process improvements and optimizations",
                    "💡 What creative solutions has Sahil implemented?",
                    "📈 Track Sahil's career progression and growth",
                    "🎯 What goals has Sahil achieved or surpassed?",
                    "🤝 How does Sahil mentor and develop others?",
                    "🔍 Show Sahil's analytical and strategic thinking",
                    "⚙️ What technical expertise does Sahil possess?",
                    "🌐 How has Sahil contributed to organizational success?"
                ]
                
                user_input = gr.Textbox(visible=False)  # Hidden textbox to store input
                
                for i, prompt in enumerate(example_prompts):
                    btn = gr.Button(
                        prompt, 
                        elem_classes=["example-btn"],
                        size="sm"
                    )
                    example_btns.append(btn)
                

            
            # Right Side - Chat Interface
            with gr.Column(scale=2):
                # Chat header
                gr.HTML("""
                <div class="chat-header">
                    <div class="chat-title">💬 Sahil's Impact Analysis</div>
                    <div class="chat-subtitle">Explore Sahil's achievements, work impact, and professional contributions</div>
                </div>
                """)
                
                # Chat messages area with overlay
                with gr.Column(elem_classes=["chat-container-wrapper"]):
                    chatbot = gr.Chatbot(
                        value=[],
                        label="Chat History",
                        height=400,
                        show_label=False,
                        elem_classes=["chat-messages"],
                        type="messages",
                        show_copy_button=True,
                        placeholder="🤖 Welcome! I'm ready to analyze Sahil's work portfolio and achievements.\n\n💡 Click an example query or ask about Sahil's impact, contributions, and professional growth."
                    )
                    
                    # Processing overlay - positioned within the chatbot area
                    processing_overlay = gr.HTML(
                        value="",
                        visible=True,
                        elem_id="processing_overlay"
                    )
                
                # Chat input section at bottom
                with gr.Column(elem_classes=["input-section"]):
                    chat_input = gr.Textbox(
                        placeholder="Ask about Sahil's achievements, work impact, contributions...",
                        lines=2,
                        show_label=False,
                        elem_classes=["chat-input"]
                    )
                    
                    with gr.Row(elem_classes=["button-row"]):
                        submit_btn = gr.Button(
                            "💬 Send Message", 
                            variant="primary", 
                            size="lg",
                            elem_classes=["send-btn"]
                        )
                        
                        clear_btn = gr.Button(
                            "🗑️ Clear Chat", 
                            variant="secondary", 
                            size="lg",
                            elem_classes=["clear-btn"]
                        )
        
        # Event handlers - Show spinner during processing
        def show_processing():
            spinner_html = """
            <div class="processing-overlay">
                <div class="spinner"></div>
                <div class="processing-text">🤖 Analyzing Sahil's work portfolio...</div>
            </div>
            """
            return (
                gr.update(elem_classes=["chat-messages", "processing"]),  # Add blur to chatbot
                gr.update(value=spinner_html, visible=True)  # Show spinner
            )
        
        def hide_processing_and_update(user_message, chat_history):
            # Process the message
            updated_chat, cleared_input, _ = process_chat_message(user_message, chat_history)
            
            return (
                gr.update(value=updated_chat, elem_classes=["chat-messages"]),  # Remove blur from chatbot
                cleared_input, 
                gr.update(value="", visible=False)  # Hide spinner
            )
        
        submit_btn.click(
            fn=show_processing,
            outputs=[chatbot, processing_overlay],
            show_progress=False
        ).then(
            fn=hide_processing_and_update,
            inputs=[chat_input, chatbot],
            outputs=[chatbot, chat_input, processing_overlay],
            show_progress=False,
            scroll_to_output=True
        )
        
        # Also handle Enter key press in the input
        chat_input.submit(
            fn=show_processing,
            outputs=[chatbot, processing_overlay],
            show_progress=False
        ).then(
            fn=hide_processing_and_update,
            inputs=[chat_input, chatbot],
            outputs=[chatbot, chat_input, processing_overlay],
            show_progress=False,
            scroll_to_output=True
        )
        
        # Clear chat functionality
        def clear_chat_history():
            """Clear the chat history and reset to initial state"""
            return [], ""  # Clear chatbot and input
        
        # Connect clear button
        clear_btn.click(
            fn=clear_chat_history,
            outputs=[chatbot, chat_input],
            show_progress=False
        )
        
        # Connect example buttons to chat input
        def create_example_handler(prompt_text):
            def handler_process_example(chat_history):
                # Remove the emoji and clean up the text
                clean_prompt = prompt_text.split(' ', 1)[1] if ' ' in prompt_text else prompt_text
                updated_chat, cleared_input, _ = process_chat_message(clean_prompt, chat_history)
                
                return (
                    gr.update(value=updated_chat, elem_classes=["chat-messages"]),  # Remove blur
                    cleared_input, 
                    gr.update(value="", visible=False)  # Hide spinner
                )
            
            return handler_process_example
        
        # Set up click handlers for each example button
        for i, (btn, prompt) in enumerate(zip(example_btns, example_prompts)):
            handler_process = create_example_handler(prompt)
            btn.click(
                fn=show_processing,
                outputs=[chatbot, processing_overlay],
                show_progress=False
            ).then(
                fn=handler_process,
                inputs=[chatbot],
                outputs=[chatbot, chat_input, processing_overlay],
                show_progress=False
            )
    
    return demo

 # Create the interface
demo = create_advanced_interface()

if __name__ == "__main__":
    import os
    
    # Get port from environment variable (Render sets this) or default to 7860
    port = int(os.environ.get("PORT", 7860))
    
    demo.launch(
        share=False,  # Set to True if you want a public link
        server_name="0.0.0.0",  # Bind to all interfaces for hosting platforms
        server_port=port,  # Use port from environment or default
        show_error=True,
        quiet=True,
        favicon_path=None,
        auth=None,  # Add authentication if needed: auth=("username", "password")
        inbrowser=False  # Don't auto-open browser to avoid SSL issues
    )