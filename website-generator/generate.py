"""
Portfolio Website Generator
Creates stunning, agency-level freelancer portfolio websites
"""

import os
import json
import re
from datetime import datetime

def generate_portfolio(data):
    """Generate a complete portfolio website from freelancer data"""

    # Extract data from Google Sheet
    full_name = data.get('full_name', 'Freelancer')
    email = data.get('email', '')
    niche = data.get('niche', 'Freelancer')
    services = data.get('services', '').split(',') if data.get('services') else []
    target_clients = data.get('target_clients', '')
    work_samples = data.get('work_samples', [])
    testimonials = data.get('testimonials', [])
    brand_colors = data.get('brand_colors', '#6366f1,#8b5cf6')
    preferred_style = data.get('preferred_style', 'modern')
    cta = data.get('cta', 'Hire Me')

    # Parse brand colors
    colors = brand_colors.split(',') if brand_colors else ['#6366f1', '#8b5cf6']
    primary_color = colors[0].strip() if len(colors) > 0 else '#6366f1'
    secondary_color = colors[1].strip() if len(colors) > 1 else '#8b5cf6'

    # Clean services list
    services = [s.strip() for s in services if s.strip()]

    # Generate slug for folder name
    slug = email.split('@')[0].replace('.', '-')

    # Create portfolio directory
    portfolio_dir = f'/workspace/portfolios/{slug}'
    os.makedirs(portfolio_dir, exist_ok=True)
    os.makedirs(f'{portfolio_dir}/assets', exist_ok=True)

    # Generate HTML
    html_content = generate_html(
        full_name=full_name,
        email=email,
        niche=niche,
        services=services,
        target_clients=target_clients,
        work_samples=work_samples,
        testimonials=testimonials,
        primary_color=primary_color,
        secondary_color=secondary_color,
        cta=cta
    )

    # Generate CSS
    css_content = generate_css(primary_color, secondary_color, preferred_style)

    # Generate JavaScript
    js_content = generate_javascript()

    # Write files
    with open(f'{portfolio_dir}/index.html', 'w') as f:
        f.write(html_content)

    with open(f'{portfolio_dir}/styles.css', 'w') as f:
        f.write(css_content)

    with open(f'{portfolio_dir}/script.js', 'w') as f:
        f.write(js_content)

    with open(f'{portfolio_dir}/data.json', 'w') as f:
        json.dump(data, f, indent=2)

    return {'success': True, 'path': portfolio_dir, 'slug': slug}


def generate_html(full_name, email, niche, services, target_clients, work_samples, testimonials, primary_color, secondary_color, cta):
    """Generate stunning HTML with agency-level design"""

    services_html = ''.join([
        f'<div class="service-card"><h3>{s}</h3></div>' for s in services
    ]) if services else '<div class="service-card"><h3>Web Development</h3></div><div class="service-card"><h3>Design</h3></div>'

    work_samples_html = ''
    if work_samples:
        for i, sample in enumerate(work_samples[:6]):  # Max 6 samples
            work_samples_html += f'''
            <div class="work-item">
                <div class="work-image" style="background: linear-gradient(135deg, {primary_color}, {secondary_color});">
                    <span class="work-number">{i+1}</span>
                </div>
                <div class="work-overlay">
                    <h4>Project {i+1}</h4>
                    <p>View Project</p>
                </div>
            </div>
            '''
    else:
        work_samples_html = '''
        <div class="work-item"><div class="work-placeholder">Project 1</div></div>
        <div class="work-item"><div class="work-placeholder">Project 2</div></div>
        <div class="work-item"><div class="work-placeholder">Project 3</div></div>
        '''

    testimonials_html = ''
    for i, testimonial in enumerate(testimonials[:3] if testimonials else []):
        testimonials_html += f'''
        <div class="testimonial-card">
            <p class="testimonial-text">"{testimonial}"</p>
            <p class="testimonial-author">- Client {i+1}</p>
        </div>
        '''

    if not testimonials_html:
        testimonials_html = '''
        <div class="testimonial-card">
            <p class="testimonial-text">"Exceptional work and professionalism. Highly recommended!"</p>
            <p class="testimonial-author">- Satisfied Client</p>
        </div>
        '''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{full_name} | {niche} Expert</title>
    <meta name="description" content="{full_name} - Professional {niche} services for {target_clients}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="#" class="logo">{full_name.split()[0]}<span class="logo-highlight">.</span></a>
            <ul class="nav-links">
                <li><a href="#about">About</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#work">Work</a></li>
                <li><a href="#testimonials">Testimonials</a></li>
                <li><a href="#contact" class="nav-cta">Let's Talk</a></li>
            </ul>
            <button class="mobile-menu-btn" aria-label="Menu">
                <span></span><span></span><span></span>
            </button>
        </div>
    </nav>

    <!-- Hero Section -->
    <header class="hero">
        <div class="hero-bg"></div>
        <div class="hero-container">
            <div class="hero-content">
                <span class="hero-badge">Available for Projects</span>
                <h1 class="hero-title">
                    Hi, I'm <span class="highlight">{full_name}</span>
                </h1>
                <h2 class="hero-subtitle">
                    <span class="typewriter" data-words="['{niche} Expert', 'Creative Problem Solver', 'Results-Driven Professional']"></span>
                </h2>
                <p class="hero-description">
                    I help {target_clients or 'businesses'} achieve their goals through exceptional {niche.lower()} solutions.
                    Let's create something amazing together.
                </p>
                <div class="hero-cta">
                    <a href="#contact" class="btn btn-primary">{cta}</a>
                    <a href="#work" class="btn btn-secondary">View My Work</a>
                </div>
                <div class="hero-stats">
                    <div class="stat">
                        <span class="stat-number">100+</span>
                        <span class="stat-label">Projects Completed</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">50+</span>
                        <span class="stat-label">Happy Clients</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">5+</span>
                        <span class="stat-label">Years Experience</span>
                    </div>
                </div>
            </div>
            <div class="hero-visual">
                <div class="hero-image-wrapper">
                    <div class="hero-shape shape-1"></div>
                    <div class="hero-shape shape-2"></div>
                    <div class="hero-avatar">
                        <span>{full_name[0].upper()}</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="scroll-indicator">
            <span>Scroll</span>
            <div class="mouse"></div>
        </div>
    </header>

    <!-- Services Section -->
    <section id="services" class="services">
        <div class="container">
            <div class="section-header">
                <span class="section-tag">What I Do</span>
                <h2 class="section-title">Services I Offer</h2>
                <p class="section-description">Comprehensive solutions tailored to your needs</p>
            </div>
            <div class="services-grid">
                {services_html}
            </div>
        </div>
    </section>

    <!-- Work Section -->
    <section id="work" class="work">
        <div class="container">
            <div class="section-header">
                <span class="section-tag">Portfolio</span>
                <h2 class="section-title">Recent Work</h2>
                <p class="section-description">A selection of my latest projects</p>
            </div>
            <div class="work-grid">
                {work_samples_html}
            </div>
        </div>
    </section>

    <!-- Testimonials Section -->
    <section id="testimonials" class="testimonials">
        <div class="container">
            <div class="section-header">
                <span class="section-tag">Testimonials</span>
                <h2 class="section-title">What Clients Say</h2>
                <p class="section-description">Trusted by businesses worldwide</p>
            </div>
            <div class="testimonials-slider">
                {testimonials_html}
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="contact">
        <div class="container">
            <div class="contact-wrapper">
                <div class="contact-content">
                    <span class="section-tag">Get In Touch</span>
                    <h2 class="section-title">Let's Work Together</h2>
                    <p class="contact-text">
                        Ready to start your project? I'd love to hear about your goals and discuss how I can help bring your vision to life.
                    </p>
                    <div class="contact-info">
                        <div class="contact-item">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                                <polyline points="22,6 12,13 2,6"></polyline>
                            </svg>
                            <span>{email}</span>
                        </div>
                    </div>
                </div>
                <div class="contact-form-wrapper">
                    <a href="https://cal.com/shazada-soban/quick-chat?overlayCalendar=true" target="_blank" class="cta-button">
                        <span>Book a Free Call</span>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                            <polyline points="12 5 19 12 12 19"></polyline>
                        </svg>
                    </a>
                    <p class="cta-note">Schedule a quick chat to discuss your project</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <a href="#" class="logo">{full_name.split()[0]}<span class="logo-highlight">.</span></a>
                    <p>Professional {niche} services</p>
                </div>
                <div class="footer-links">
                    <a href="#about">About</a>
                    <a href="#services">Services</a>
                    <a href="#work">Work</a>
                    <a href="#contact">Contact</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; {datetime.now().year} {full_name}. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>'''


def generate_css(primary_color, secondary_color, style):
    """Generate stunning CSS with animations"""

    return f'''/* ========================================
   PORTFOLIO STYLES - AGENCY LEVEL DESIGN
   ======================================== */

:root {{
    --primary: {primary_color};
    --secondary: {secondary_color};
    --dark: #0f172a;
    --darker: #020617;
    --light: #f8fafc;
    --gray-100: #f1f5f9;
    --gray-200: #e2e8f0;
    --gray-300: #cbd5e1;
    --gray-400: #94a3b8;
    --gray-500: #64748b;
    --gray-600: #475569;
    --gray-700: #334155;
    --gradient: linear-gradient(135deg, var(--primary), var(--secondary));
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--light);
    color: var(--dark);
    line-height: 1.6;
    overflow-x: hidden;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
}}

/* Navigation */
.navbar {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    padding: 20px 0;
    transition: all 0.3s ease;
}}

.navbar.scrolled {{
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    padding: 15px 0;
}}

.nav-container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo {{
    font-size: 28px;
    font-weight: 800;
    color: var(--dark);
    text-decoration: none;
    font-family: 'Playfair Display', serif;
}}

.logo-highlight {{
    color: var(--primary);
}}

.nav-links {{
    display: flex;
    list-style: none;
    gap: 40px;
    align-items: center;
}}

.nav-links a {{
    text-decoration: none;
    color: var(--gray-600);
    font-weight: 500;
    font-size: 15px;
    transition: color 0.3s ease;
}}

.nav-links a:hover {{
    color: var(--primary);
}}

.nav-cta {{
    background: var(--gradient);
    color: white !important;
    padding: 10px 24px;
    border-radius: 50px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.nav-cta:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
}}

.mobile-menu-btn {{
    display: none;
    flex-direction: column;
    gap: 5px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 5px;
}}

.mobile-menu-btn span {{
    width: 25px;
    height: 2px;
    background: var(--dark);
    transition: all 0.3s ease;
}}

/* Hero Section */
.hero {{
    min-height: 100vh;
    display: flex;
    align-items: center;
    position: relative;
    padding: 120px 0 80px;
    overflow: hidden;
}}

.hero-bg {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(ellipse at top right, rgba(99, 102, 241, 0.1), transparent 50%),
                radial-gradient(ellipse at bottom left, rgba(139, 92, 246, 0.1), transparent 50%);
}}

.hero-container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 60px;
    align-items: center;
    position: relative;
    z-index: 1;
}}

.hero-badge {{
    display: inline-block;
    background: rgba(99, 102, 241, 0.1);
    color: var(--primary);
    padding: 8px 16px;
    border-radius: 50px;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 24px;
}}

.hero-title {{
    font-size: clamp(40px, 5vw, 64px);
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 16px;
    color: var(--dark);
}}

.highlight {{
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.hero-subtitle {{
    font-size: 24px;
    color: var(--gray-500);
    margin-bottom: 24px;
    min-height: 36px;
}}

.typewriter {{
    border-right: 2px solid var(--primary);
    animation: blink 1s infinite;
}}

@keyframes blink {{
    0%, 50% {{ border-color: var(--primary); }}
    51%, 100% {{ border-color: transparent; }}
}}

.hero-description {{
    font-size: 18px;
    color: var(--gray-500);
    margin-bottom: 40px;
    max-width: 500px;
}}

.hero-cta {{
    display: flex;
    gap: 16px;
    margin-bottom: 60px;
}}

.btn {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 16px 32px;
    border-radius: 50px;
    font-size: 16px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
}}

.btn-primary {{
    background: var(--gradient);
    color: white;
    border: none;
}}

.btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
}}

.btn-secondary {{
    background: white;
    color: var(--dark);
    border: 2px solid var(--gray-200);
}}

.btn-secondary:hover {{
    border-color: var(--primary);
    color: var(--primary);
}}

.hero-stats {{
    display: flex;
    gap: 40px;
}}

.stat {{
    text-align: left;
}}

.stat-number {{
    display: block;
    font-size: 36px;
    font-weight: 800;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.stat-label {{
    font-size: 14px;
    color: var(--gray-500);
}}

.hero-visual {{
    position: relative;
}}

.hero-image-wrapper {{
    position: relative;
    width: 100%;
    aspect-ratio: 1;
    max-width: 400px;
}}

.hero-shape {{
    position: absolute;
    border-radius: 50%;
}}

.shape-1 {{
    width: 100%;
    height: 100%;
    background: var(--gradient);
    opacity: 0.1;
    animation: pulse 4s ease-in-out infinite;
}}

.shape-2 {{
    width: 80%;
    height: 80%;
    top: 10%;
    left: 10%;
    background: var(--gradient);
    opacity: 0.2;
    animation: pulse 4s ease-in-out infinite 0.5s;
}}

@keyframes pulse {{
    0%, 100% {{ transform: scale(1); opacity: 0.1; }}
    50% {{ transform: scale(1.05); opacity: 0.2; }}
}}

.hero-avatar {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 200px;
    height: 200px;
    background: var(--gradient);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 72px;
    font-weight: 800;
    color: white;
    font-family: 'Playfair Display', serif;
}}

.scroll-indicator {{
    position: absolute;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    color: var(--gray-400);
    font-size: 12px;
}}

.mouse {{
    width: 24px;
    height: 40px;
    border: 2px solid var(--gray-300);
    border-radius: 12px;
    position: relative;
}}

.mouse::before {{
    content: '';
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    width: 4px;
    height: 8px;
    background: var(--primary);
    border-radius: 2px;
    animation: scroll 2s infinite;
}}

@keyframes scroll {{
    0% {{ opacity: 1; top: 8px; }}
    100% {{ opacity: 0; top: 20px; }}
}}

/* Section Styles */
section {{
    padding: 100px 0;
}}

.section-header {{
    text-align: center;
    margin-bottom: 60px;
}}

.section-tag {{
    display: inline-block;
    background: rgba(99, 102, 241, 0.1);
    color: var(--primary);
    padding: 8px 20px;
    border-radius: 50px;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 16px;
}}

.section-title {{
    font-size: clamp(32px, 4vw, 48px);
    font-weight: 800;
    color: var(--dark);
    margin-bottom: 16px;
}}

.section-description {{
    font-size: 18px;
    color: var(--gray-500);
    max-width: 600px;
    margin: 0 auto;
}}

/* Services */
.services {{
    background: white;
}}

.services-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
}}

.service-card {{
    background: var(--light);
    padding: 40px 30px;
    border-radius: 20px;
    text-align: center;
    transition: all 0.3s ease;
    border: 1px solid var(--gray-100);
}}

.service-card:hover {{
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border-color: var(--primary);
}}

.service-card h3 {{
    font-size: 20px;
    color: var(--dark);
    font-weight: 600;
}}

/* Work */
.work {{
    background: var(--gray-100);
}}

.work-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
}}

.work-item {{
    position: relative;
    aspect-ratio: 4/3;
    border-radius: 16px;
    overflow: hidden;
    cursor: pointer;
}}

.work-image {{
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.work-number {{
    font-size: 48px;
    font-weight: 800;
    color: white;
    opacity: 0.5;
}}

.work-placeholder {{
    width: 100%;
    height: 100%;
    background: var(--gradient);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
}}

.work-overlay {{
    position: absolute;
    inset: 0;
    background: rgba(15, 23, 42, 0.9);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.work-item:hover .work-overlay {{
    opacity: 1;
}}

.work-overlay h4 {{
    color: white;
    font-size: 24px;
    margin-bottom: 8px;
}}

.work-overlay p {{
    color: var(--gray-300);
}}

/* Testimonials */
.testimonials {{
    background: white;
}}

.testimonials-slider {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
}}

.testimonial-card {{
    background: var(--light);
    padding: 40px;
    border-radius: 20px;
    border: 1px solid var(--gray-100);
}}

.testimonial-text {{
    font-size: 18px;
    color: var(--gray-600);
    margin-bottom: 20px;
    font-style: italic;
    line-height: 1.8;
}}

.testimonial-author {{
    color: var(--primary);
    font-weight: 600;
}}

/* Contact */
.contact {{
    background: var(--dark);
    color: white;
}}

.contact-wrapper {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
    align-items: center;
}}

.contact .section-tag {{
    background: rgba(255, 255, 255, 0.1);
    color: white;
}}

.contact .section-title {{
    color: white;
}}

.contact-text {{
    font-size: 18px;
    color: var(--gray-400);
    margin-bottom: 30px;
}}

.contact-info {{
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

.contact-item {{
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--gray-300);
}}

.contact-item svg {{
    color: var(--primary);
}}

.contact-form-wrapper {{
    background: rgba(255, 255, 255, 0.05);
    padding: 60px;
    border-radius: 24px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

.cta-button {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    width: 100%;
    padding: 24px 48px;
    background: var(--gradient);
    color: white;
    text-decoration: none;
    font-size: 20px;
    font-weight: 700;
    border-radius: 16px;
    transition: all 0.3s ease;
}}

.cta-button:hover {{
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.4);
}}

.cta-note {{
    margin-top: 20px;
    color: var(--gray-400);
    font-size: 14px;
}}

/* Footer */
.footer {{
    background: var(--darker);
    padding: 60px 0 30px;
}}

.footer-content {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
}}

.footer-brand p {{
    color: var(--gray-500);
    margin-top: 8px;
}}

.footer-links {{
    display: flex;
    gap: 30px;
}}

.footer-links a {{
    color: var(--gray-400);
    text-decoration: none;
    transition: color 0.3s ease;
}}

.footer-links a:hover {{
    color: var(--primary);
}}

.footer-bottom {{
    text-align: center;
    padding-top: 30px;
    border-top: 1px solid var(--gray-700);
}}

.footer-bottom p {{
    color: var(--gray-500);
    font-size: 14px;
}}

/* Responsive */
@media (max-width: 768px) {{
    .nav-links {{
        display: none;
    }}

    .mobile-menu-btn {{
        display: flex;
    }}

    .hero-container {{
        grid-template-columns: 1fr;
        text-align: center;
    }}

    .hero-content {{
        order: 2;
    }}

    .hero-visual {{
        order: 1;
        margin-bottom: 40px;
    }}

    .hero-image-wrapper {{
        max-width: 250px;
        margin: 0 auto;
    }}

    .hero-avatar {{
        width: 150px;
        height: 150px;
        font-size: 56px;
    }}

    .hero-cta {{
        justify-content: center;
        flex-wrap: wrap;
    }}

    .hero-stats {{
        justify-content: center;
    }}

    .contact-wrapper {{
        grid-template-columns: 1fr;
        text-align: center;
    }}

    .footer-content {{
        flex-direction: column;
        gap: 30px;
    }}
}}

/* Animations */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

section {{
    animation: fadeInUp 0.8s ease-out;
}}
'''


def generate_javascript():
    """Generate JavaScript for the portfolio website"""
    return '''/**
 * Portfolio Website JavaScript
 * Handles animations, interactions, and typewriter effect
 */

// Typewriter Effect
class Typewriter {
    constructor(element, words, wait = 3000) {
        this.element = element;
        this.words = words;
        this.wait = parseInt(wait, 10);
        this.wordIndex = 0;
        this.txt = '';
        this.isDeleting = false;
        this.type();
    }

    type() {
        const current = this.wordIndex % this.words.length;
        const fullTxt = this.words[current];

        if (this.isDeleting) {
            this.txt = fullTxt.substring(0, this.txt.length - 1);
        } else {
            this.txt = fullTxt.substring(0, this.txt.length + 1);
        }

        this.element.innerHTML = this.txt;

        let typeSpeed = 50;

        if (this.isDeleting) {
            typeSpeed /= 2;
        }

        if (!this.isDeleting && this.txt === fullTxt) {
            typeSpeed = this.wait;
            this.isDeleting = true;
        } else if (this.isDeleting && this.txt === '') {
            this.isDeleting = false;
            this.wordIndex++;
            typeSpeed = 500;
        }

        setTimeout(() => this.type(), typeSpeed);
    }
}

// Initialize Typewriter
document.addEventListener('DOMContentLoaded', () => {
    const typewriterElement = document.querySelector('.typewriter');
    if (typewriterElement) {
        const words = typewriterElement.getAttribute('data-words').split(',');
        new Typewriter(typewriterElement, words);
    }

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.service-card, .work-item, .testimonial-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Add animation class
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);

    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
        });
    }

    // Counter animation for stats
    const animateCounters = () => {
        const counters = document.querySelectorAll('.stat-number');
        counters.forEach(counter => {
            const target = parseInt(counter.textContent);
            const increment = target / 50;
            let current = 0;

            const updateCounter = () => {
                if (current < target) {
                    current += increment;
                    counter.textContent = Math.ceil(current) + '+';
                    setTimeout(updateCounter, 30);
                } else {
                    counter.textContent = target + '+';
                }
            };

            updateCounter();
        });
    };

    // Trigger counter animation when hero is visible
    const heroObserver = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
            animateCounters();
            heroObserver.disconnect();
        }
    });
    heroObserver.observe(document.querySelector('.hero'));
});

// Parallax effect for shapes
document.addEventListener('mousemove', (e) => {
    const shapes = document.querySelectorAll('.hero-shape');
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;

    shapes.forEach((shape, index) => {
        const speed = (index + 1) * 10;
        const xOffset = (x - 0.5) * speed;
        const yOffset = (y - 0.5) * speed;
        shape.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
    });
});
'''