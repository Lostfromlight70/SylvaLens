import os

files = ['weddings.html', 'portraits.html', 'sports.html',
         'ceremonies.html', 'pre-weddings.html', 'creative.html']
issues = []

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'function handleImageError(' not in content:
            issues.append(f'{file}: Missing handleImageError function')
        if 'function retryLoadImage(' not in content:
            issues.append(f'{file}: Missing retryLoadImage function')
        if 'reload-btn' not in content:
            issues.append(f'{file}: Missing reload-btn elements')

if issues:
    print('ISSUES FOUND:')
    for issue in issues:
        print(f'  - {issue}')
else:
    print('✓ All gallery pages have proper reload functionality implemented')

# Check CSS
css_file = 'style.css'
if os.path.exists(css_file):
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()

    css_issues = []
    if '.reload-btn' not in css_content:
        css_issues.append('Missing .reload-btn styles')
    if '.portfolio-item.error' not in css_content:
        css_issues.append('Missing .portfolio-item.error styles')
    if '.error-icon' not in css_content:
        css_issues.append('Missing .error-icon styles')
    if '.error-text' not in css_content:
        css_issues.append('Missing .error-text styles')

    if css_issues:
        print('CSS ISSUES:')
        for issue in css_issues:
            print(f'  - {issue}')
    else:
        print('✓ CSS styling for error states and reload button is present')
