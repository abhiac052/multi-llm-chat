"""
Simple script to convert PROJECT_REPORT.md to PDF using reportlab
Install: pip install reportlab markdown2
"""

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.lib.colors import HexColor
    import re
    
    # Read markdown file
    with open('PROJECT_REPORT.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF
    pdf_file = 'PROJECT_REPORT.pdf'
    doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for PDF elements
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=HexColor('#667eea'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#764ba2'),
        spaceAfter=10,
        spaceBefore=10
    )
    
    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=HexColor('#667eea'),
        spaceAfter=8,
        spaceBefore=8
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=6
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=8,
        leftIndent=20,
        spaceAfter=10
    )
    
    # Parse markdown and add to PDF
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            story.append(Spacer(1, 0.1*inch))
            i += 1
            continue
        
        # Title (first H1)
        if line.startswith('# ') and i == 0:
            story.append(Paragraph(line[2:], title_style))
            story.append(Spacer(1, 0.3*inch))
        
        # H1
        elif line.startswith('## '):
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(line[3:], h1_style))
        
        # H2
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], h2_style))
        
        # H3
        elif line.startswith('#### '):
            story.append(Paragraph(line[5:], h3_style))
        
        # Code block
        elif line.startswith('```'):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if code_lines:
                code_text = '\n'.join(code_lines)
                story.append(Preformatted(code_text, code_style))
        
        # Bullet points
        elif line.startswith('- ') or line.startswith('* '):
            text = line[2:].replace('✅', '✓').replace('❌', '✗').replace('[ ]', '☐').replace('[x]', '☑')
            story.append(Paragraph(f"• {text}", body_style))
        
        # Numbered list
        elif re.match(r'^\d+\.', line):
            text = re.sub(r'^\d+\.\s*', '', line)
            story.append(Paragraph(text, body_style))
        
        # Regular paragraph
        else:
            # Clean up special characters and markdown
            text = line
            # Handle bold text properly
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            # Handle inline code
            text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
            # Escape special XML characters
            text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Restore HTML tags we want
            text = text.replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
            text = text.replace('&lt;font face="Courier"&gt;', '<font face="Courier">').replace('&lt;/font&gt;', '</font>')
            try:
                story.append(Paragraph(text, body_style))
            except:
                # If paragraph fails, add as plain text
                story.append(Spacer(1, 0.05*inch))
        
        i += 1
    
    # Build PDF
    doc.build(story)
    
    print("✅ PDF created successfully: PROJECT_REPORT.pdf")
    print("📄 File location:", os.path.abspath(pdf_file))
    
except ImportError:
    print("❌ Missing required package. Please install:")
    print("   pip install reportlab")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
