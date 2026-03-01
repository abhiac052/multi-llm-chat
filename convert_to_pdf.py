"""
Script to convert PROJECT_REPORT.md to PDF
Install required package: pip install markdown2 weasyprint
"""

try:
    import markdown2
    from weasyprint import HTML
    import os
    
    # Read the markdown file
    with open('PROJECT_REPORT.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(markdown_content, extras=['tables', 'fenced-code-blocks'])
    
    # Add CSS styling
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
                color: #333;
            }}
            h1 {{
                color: #667eea;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
                margin-top: 30px;
            }}
            h2 {{
                color: #764ba2;
                margin-top: 25px;
                border-bottom: 2px solid #e0e0e0;
                padding-bottom: 8px;
            }}
            h3 {{
                color: #667eea;
                margin-top: 20px;
            }}
            code {{
                background: #f5f5f5;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }}
            pre {{
                background: #f5f5f5;
                padding: 15px;
                border-radius: 5px;
                border-left: 4px solid #667eea;
                overflow-x: auto;
            }}
            pre code {{
                background: none;
                padding: 0;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background: #667eea;
                color: white;
            }}
            ul, ol {{
                margin: 10px 0;
                padding-left: 30px;
            }}
            li {{
                margin: 5px 0;
            }}
            blockquote {{
                border-left: 4px solid #667eea;
                padding-left: 20px;
                margin: 20px 0;
                color: #666;
            }}
            .page-break {{
                page-break-after: always;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert HTML to PDF
    HTML(string=styled_html).write_pdf('PROJECT_REPORT.pdf')
    
    print("✅ PDF created successfully: PROJECT_REPORT.pdf")
    
except ImportError as e:
    print("❌ Missing required packages. Please install them:")
    print("   pip install markdown2 weasyprint")
    print("\nNote: WeasyPrint requires GTK3 libraries:")
    print("   Windows: Download from https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases")
    print("   Mac: brew install python3 cairo pango gdk-pixbuf libffi")
    print("   Linux: sudo apt-get install python3-dev python3-pip python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info")
except Exception as e:
    print(f"❌ Error: {e}")
