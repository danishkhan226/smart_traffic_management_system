import zipfile
import os
import xml.etree.ElementTree as ET

docx_path = 'conference-Papertemplate.docx'

print("=" * 80)
print(f"Analyzing: {docx_path}")
print("=" * 80)

try:
    # Check if file exists
    if not os.path.exists(docx_path):
        print(f"Error: File not found at {docx_path}")
        exit(1)
    
    # Open as ZIP archive
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        print("\nFiles in the DOCX archive:")
        print("-" * 80)
        for name in zip_ref.namelist():
            print(f"  {name}")
        
        # Try to extract and read document.xml
        print("\n" + "=" * 80)
        print("Attempting to read document content...")
        print("=" * 80)
        
        # Look for the main document
        doc_xml_paths = ['word/document.xml', 'document.xml']
        content_found = False
        
        for doc_path in doc_xml_paths:
            if doc_path in zip_ref.namelist():
                print(f"\nFound: {doc_path}")
                with zip_ref.open(doc_path) as xml_file:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    
                    # Extract all text nodes
                    namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                    
                    paragraphs = root.findall('.//w:p', namespace)
                    print(f"\nFound {len(paragraphs)} paragraphs\n")
                    
                    for i, para in enumerate(paragraphs, 1):
                        texts = para.findall('.//w:t', namespace)
                        para_text = ''.join([t.text for t in texts if t.text])
                        if para_text.strip():
                            print(f"[Paragraph {i}]")
                            print(para_text)
                            print()
                    
                    content_found = True
                    break
        
        if not content_found:
            print("\nCould not find document.xml in standard locations.")
            print("This might not be a valid DOCX file.")
            
except zipfile.BadZipFile:
    print("Error: This is not a valid ZIP/DOCX file")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
