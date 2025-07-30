# Monte Carlo Data Quality Demo - GitHub Pages

This directory contains the GitHub Pages website for the Monte Carlo Data Quality Demo project.

## Files

- `index.html` - Main website page with comprehensive project showcase
- `styles.css` - Modern CSS styling with responsive design
- `script.js` - Interactive JavaScript functionality
- `README.md` - This documentation file

## Features

### 🎨 Modern Design
- Clean, professional layout
- Responsive design for all devices
- Interactive elements and animations
- Hero section with dashboard preview

### 📱 Mobile-First
- Hamburger menu for mobile navigation
- Optimized layouts for all screen sizes
- Touch-friendly interactions

### ⚡ Interactive Elements
- Live dashboard preview with tabs
- Copy-to-clipboard functionality for code snippets
- Smooth scrolling navigation
- Animated counters and progress indicators

### 🚀 Performance
- Optimized CSS and JavaScript
- Service worker ready
- Fast loading times
- SEO optimized

## Development

To preview the site locally:

1. Install Jekyll (if using Jekyll themes):
   ```bash
   gem install jekyll bundler
   ```

2. Serve the site:
   ```bash
   bundle exec jekyll serve
   ```

3. Open http://localhost:4000 in your browser

## GitHub Pages Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the main branch.

**Live URL**: https://b8234.github.io/monte-carlo-demo/

## Content Sections

1. **Hero** - Project introduction with dashboard preview
2. **Learning Objectives** - Educational goals and outcomes
3. **Features** - Key capabilities and benefits
4. **Live Demo** - Step-by-step setup instructions
5. **Architecture** - Technical overview and components
6. **Code Quality** - Code examples and best practices
7. **Footer** - Additional resources and links

## Customization

### Colors
The CSS uses CSS custom properties (variables) for easy theme customization:

```css
:root {
  --primary: #2563eb;
  --secondary: #64748b;
  --success: #059669;
  --warning: #d97706;
  --error: #dc2626;
}
```

### Navigation
Update the navigation menu in `index.html` and `script.js` for new sections.

### Content
All content is in `index.html` with clear section markers for easy editing.

## Analytics

To add Google Analytics:
1. Update `_config.yml` with your tracking ID
2. Add the analytics script to `index.html`

## SEO

The site includes:
- Meta tags for social sharing
- Open Graph protocol
- Structured data
- Semantic HTML

## Accessibility

- ARIA labels and roles
- Keyboard navigation support
- Screen reader friendly
- High contrast compliance

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## License

This website is part of the Monte Carlo Data Quality Demo project and follows the same licensing terms.
