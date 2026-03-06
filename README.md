# 🖼️ Background Remover

Remove image backgrounds instantly with AI-powered precision. Upload any image and download a clean PNG with transparent background.

## Features

✨ **AI-Powered** - Advanced background removal using rembg AI model
⚡ **Ultra Fast** - Process images in seconds
🆓 **100% Free** - No limits, no watermarks, completely free forever
🖼️ **Ultra HD Quality** - High-quality transparent PNG output
📱 **Works Everywhere** - Desktop, tablet, mobile - fully responsive
🔒 **Private** - Images are processed and deleted immediately
📦 **Multiple Formats** - PNG, JPG, GIF, BMP, WEBP support
📊 **Large Files** - Up to 50MB file size support

## Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Flask, Python
- **AI:** rembg (AI-powered background removal)
- **Hosting:** Vercel (Backend), GitHub Pages (Frontend)
- **Libraries:** 
  - Flask
  - Flask-CORS
  - rembg
  - Pillow
  - Werkzeug

## Installation

### Local Development

1. Clone the repository
```bash
git clone https://github.com/hitters999/background-remover.git
cd background-remover
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run Flask app
```bash
python app.py
```

5. Open `index.html` in your browser (or use a local server)
```bash
python -m http.server 8000
```

## Deployment

### Vercel Deployment (Backend)

1. Push code to GitHub
2. Go to Vercel dashboard
3. Click "New Project"
4. Import your GitHub repository
5. Vercel will auto-detect Flask app
6. Click "Deploy"
7. Copy the deployment URL
8. Update API_URL in `background-remover.html` with your Vercel URL

### GitHub Pages (Frontend)

1. The HTML file can be served directly from GitHub Pages
2. Place `background-remover.html` in your repo
3. Enable GitHub Pages in repository settings
4. Access via: `https://yourusername.github.io/repo/background-remover.html`

## API Usage

### Remove Background Endpoint

**POST** `/api/remove`

**Request:**
```
Form Data:
- image: (file) - Image file to process
```

**Response:**
```
Content-Type: image/png
Body: PNG image with transparent background
```

**Example cURL:**
```bash
curl -X POST -F "image=@your_image.jpg" \
  https://your-vercel-url.vercel.app/api/remove \
  -o output.png
```

### Health Check

**GET** `/api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "background-remover",
  "version": "1.0.0"
}
```

### Service Statistics

**GET** `/api/stats`

**Response:**
```json
{
  "service": "Background Remover",
  "ai_model": "rembg",
  "supported_formats": ["png", "jpg", "jpeg", "gif", "bmp", "webp"],
  "max_file_size_mb": 50,
  "processing": "AI-powered with rembg",
  "output_format": "PNG with transparency",
  "quality": "Ultra HD"
}
```

## File Structure

```
background-remover/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
├── background-remover.html # Frontend UI
├── index.html            # Homepage (optional)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## How It Works

1. **User uploads image** → Frontend validates file
2. **Image sent to backend** → Flask receives the file
3. **AI processing** → rembg removes background
4. **Image optimization** → Pillow optimizes PNG
5. **User downloads** → PNG with transparent background

## Supported Formats

**Input:** PNG, JPG, JPEG, GIF, BMP, WEBP
**Output:** PNG (with transparency)
**Max Size:** 50MB

## Performance

- Average processing time: 2-5 seconds
- Supports images up to 50MB
- Ultra HD quality output
- No quality loss
- Instant download

## API Rate Limiting

- Free tier: Unlimited requests
- No authentication required
- CORS enabled for cross-origin requests

## Troubleshooting

### Image not processing
- Check file size (max 50MB)
- Ensure image format is supported
- Check internet connection
- Try a different browser

### API connection error
- Verify Vercel deployment URL
- Check CORS settings
- Ensure backend is running
- Check browser console for errors

### Low quality output
- Ensure input image is clear
- Try a higher resolution image
- Check for image compression

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Share feature requests

## License

MIT License - Free to use, modify, and distribute

## Author

Toolyfi - Free Online Tools & World News

## Support

For issues, questions, or suggestions:
- GitHub Issues: Create an issue in this repository
- Email: contact@toolyfi.com
- Website: https://toolyfi.com

## Updates

- v1.0.0 (2026) - Initial release with AI background removal

---

**Made with ❤️ by Toolyfi**

100% Free • No Limits • AI-Powered
