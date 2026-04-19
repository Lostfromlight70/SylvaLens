# Sylva Lens - Photography Portfolio Website

A modern, responsive photography portfolio website for Sylva Lens featuring image upload functionality and a sleek dark theme.

## Features

- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Dark Theme**: Elegant black and gold color scheme
- **Image Upload**: Interactive portfolio management with drag-and-drop style upload areas
- **Contact Form**: Functional contact form with Nigerian phone number formatting
- **Smooth Animations**: CSS transitions and hover effects throughout
- **Local Storage**: Uploaded images persist between browser sessions

## Portfolio Categories

- Weddings
- Portraits
- Sports
- Ceremonies
- Pre Wedding
- Creative
- Product Shoot

## Technical Implementation

- **HTML5**: Semantic markup with accessibility considerations
- **CSS3**: Modern styling with CSS Grid, Flexbox, and custom properties
- **Vanilla JavaScript**: No frameworks, pure JavaScript for interactivity
- **Local Storage API**: Client-side image persistence
- **FileReader API**: Image preview functionality

## How to Use

1. **View Portfolio**: Browse through different photography categories
2. **Upload Images**: Click on any "Click to upload" area to add portfolio images
3. **Delete Images**: Click the ✕ button to remove uploaded images
4. **Contact**: Use the contact form to get in touch

## Running the Website

```bash
# Navigate to the project directory
cd "Sylva Lens"

# Start a local server (Python 3)
python -m http.server 8000

# Or with Node.js
npx serve .

# Open in browser
# http://localhost:8000/index.html
```

## GitHub Deployment

1. Install Git on Windows if it is not already installed: https://git-scm.com/download/win
2. Initialize the local repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
3. Create a new GitHub repository and add it as a remote:
   ```bash
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git branch -M main
   git push -u origin main
   ```
4. In Netlify, connect the GitHub repository and deploy the `main` branch for automatic updates on each push.

## Browser Support

- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+

## File Structure

```
Sylva Lens/
├── index.html         # Main website file
├── style.css          # Styling and animations
├── Images/            # Image storage directory
├── Weddings/          # Category folders
├── Portraits/
├── Sports/
├── Ceremonies/
├── Creative/
├── Pre weddings/
└── Product shoot/
```

## Contact Form

The contact form submits to Formspree (https://formspree.io/f/xlgpyzbe). Update the action URL if you want to use a different service.

## Customization

- **Colors**: Modify CSS custom properties in `:root` for theme changes
- **Fonts**: Update Google Fonts links in the HTML head
- **Categories**: Add or remove portfolio categories by editing the HTML
- **Contact**: Change the Formspree endpoint for different email handling

## License

© 2026 Sylva Lens. All rights reserved.