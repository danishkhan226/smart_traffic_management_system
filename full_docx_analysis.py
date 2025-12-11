import zipfile
import xml.etree.ElementTree as ET

docx_path = 'conference-Papertemplate.docx'

print("=" * 80)
print("COMPLETE DOCX FILE ANALYSIS")
print("=" * 80)

with zipfile.ZipFile(docx_path, 'r') as zip_ref:
    print("\n1. ALL FILES IN ARCHIVE:")
    print("-" * 80)
    for name in sorted(zip_ref.namelist()):
        info = zip_ref.getinfo(name)
        print(f"  {name} ({info.file_size} bytes)")
    
    # Check all XML files for text content
    print("\n2. SEARCHING FOR TEXT CONTENT:")
    print("-" * 80)
    
    for filename in zip_ref.namelist():
        if filename.endswith('.xml'):
            try:
                with zip_ref.open(filename) as xml_file:
                    content = xml_file.read().decode('utf-8')
                    
                    # Look for text content
                    tree = ET.fromstring(content)
                    
                    # Find all elements with text
                    all_text = []
                    for elem in tree.iter():
                        if elem.text and elem.text.strip():
                            all_text.append(elem.text.strip())
                        if elem.tail and elem.tail.strip():
                            all_text.append(elem.tail.strip())
                    
                    if all_text:
                        print(f"\n{filename}:")
                        for text in all_text[:20]:  # Show first 20 text elements
                            if len(text) > 100:
                                print(f"  - {text[:100]}...")
                            else:
                                print(f"  - {text}")
                        if len(all_text) > 20:
                            print(f"  ... and {len(all_text) - 20} more text elements")
            except:
                pass
    
    # Also check for any .rels files that might indicate structure
    print("\n3. DOCUMENT RELATIONSHIPS:")
    print("-" * 80)
    if '_rels/.rels' in zip_ref.namelist():
        with zip_ref.open('_rels/.rels') as f:
            print(f.read().decode('utf-8'))
