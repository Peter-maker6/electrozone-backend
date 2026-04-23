from app import create_app, db
from models.models import User, Category, Product

app = create_app()

# Initialize database with products when server starts
def init_database():
    """Initialize the database with tables and seed data."""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Check if data already exists
        if Category.query.first():
            print("✓ Database already has data, skipping seed")
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@electrozone.com',
            full_name='Administrator',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create categories
        categories = [
            Category(
                name='Laptops & Computers',
                description='Shop the latest laptops, desktops, and computer accessories',
                image_url='https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400'
            ),
            Category(
                name='Smartphones & Tablets',
                description='Latest smartphones, tablets, and mobile accessories',
                image_url='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400'
            ),
            Category(
                name='TV & Home Entertainment',
                description='Smart TVs, soundbars, and home theater systems',
                image_url='https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400'
            ),
            Category(
                name='Gaming',
                description='Gaming consoles, PC gaming, and accessories',
                image_url='https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400'
            ),
            Category(
                name='Audio & Headphones',
                description='Premium headphones, earbuds, and audio equipment',
                image_url='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'
            ),
            Category(
                name='Cameras & Photography',
                description='Digital cameras, DSLR, mirrorless, and accessories',
                image_url='https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400'
            ),
            Category(
                name='Smart Home',
                description='Smart devices, automation, and IoT products',
                image_url='https://images.unsplash.com/photo-1558002038-1055907df827?w=400'
            ),
            Category(
                name='Accessories',
                description='Cables, chargers, cases, and other electronic accessories',
                image_url='https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400'
            )
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        print("✓ Categories created successfully")
        
        # Create products (all 39 products including the 20 new ones)
        products = [
            # Original Products
            Product(
                name='MacBook Pro 16" M3 Max',
                description='Apple MacBook Pro with M3 Max chip, 36GB RAM, 1TB SSD. The most powerful MacBook ever with incredible performance and battery life.',
                price=349999.00,
                original_price=399999.00,
                stock_quantity=15,
                category_id=1,
                brand='Apple',
                model='MacBook Pro 16" M3 Max',
                image_url='https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400',
                is_featured=True,
                rating=4.9,
                review_count=256
            ),
            Product(
                name='Dell XPS 15 OLED',
                description='Dell XPS 15 with 13th Gen Intel Core i9, 32GB RAM, 1TB SSD, 15.6" 3.5K OLED display. Premium Windows laptop.',
                price=189999.00,
                original_price=219999.00,
                stock_quantity=20,
                category_id=1,
                brand='Dell',
                model='XPS 15 OLED',
                image_url='https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400',
                is_featured=True,
                rating=4.7,
                review_count=189
            ),
            Product(
                name='HP Spectre x360',
                description='HP Spectre x360 2-in-1 laptop with Intel Core i7, 16GB RAM, 512GB SSD, 14" touchscreen display.',
                price=129999.00,
                original_price=149999.00,
                stock_quantity=25,
                category_id=1,
                brand='HP',
                model='Spectre x360',
                image_url='https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=400',
                is_featured=False,
                rating=4.5,
                review_count=142
            ),
            Product(
                name='iPhone 15 Pro Max',
                description='iPhone 15 Pro Max with A17 Pro chip, 256GB storage, titanium design, advanced camera system with 5x optical zoom.',
                price=169999.00,
                original_price=189999.00,
                stock_quantity=30,
                category_id=2,
                brand='Apple',
                model='iPhone 15 Pro Max',
                image_url='https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400',
                is_featured=True,
                rating=4.8,
                review_count=523
            ),
            Product(
                name='Samsung Galaxy S24 Ultra',
                description='Samsung Galaxy S24 Ultra with Snapdragon 8 Gen 3, 512GB storage, S Pen, 200MP camera, AI features.',
                price=149999.00,
                original_price=169999.00,
                stock_quantity=25,
                category_id=2,
                brand='Samsung',
                model='Galaxy S24 Ultra',
                image_url='https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400',
                is_featured=True,
                rating=4.7,
                review_count=412
            ),
            Product(
                name='Google Pixel 8 Pro',
                description='Google Pixel 8 Pro with Tensor G3, 256GB storage, 50MP camera, 7 years of updates, AI features.',
                price=99999.00,
                original_price=119999.00,
                stock_quantity=20,
                category_id=2,
                brand='Google',
                model='Pixel 8 Pro',
                image_url='https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400',
                is_featured=False,
                rating=4.6,
                review_count=287
            ),
            Product(
                name='Samsung 77" OLED 4K Smart TV',
                description='Samsung 77" OLED 4K Smart TV with Neural Quantum Processor, Dolby Atmos, Gaming Hub, and One Connect.',
                price=299999.00,
                original_price=349999.00,
                stock_quantity=10,
                category_id=3,
                brand='Samsung',
                model='S95C OLED',
                image_url='https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400',
                is_featured=True,
                rating=4.9,
                review_count=178
            ),
            Product(
                name='LG 65" C3 OLED evo',
                description='LG 65" C3 OLED evo with self-lit pixels, Dolby Vision, webOS 23, gaming optimization.',
                price=199999.00,
                original_price=249999.00,
                stock_quantity=12,
                category_id=3,
                brand='LG',
                model='C3 OLED evo',
                image_url='https://images.unsplash.com/photo-1461151304267-38535e780c79?w=400',
                is_featured=True,
                rating=4.8,
                review_count=156
            ),
            Product(
                name='PlayStation 5 Slim',
                description='PlayStation 5 Slim Console with 1TB SSD, DualSense controller, 4K gaming, ray tracing support.',
                price=89999.00,
                original_price=99999.00,
                stock_quantity=15,
                category_id=4,
                brand='Sony',
                model='PS5 Slim',
                image_url='https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400',
                is_featured=True,
                rating=4.9,
                review_count=892
            ),
            Product(
                name='Xbox Series X',
                description='Xbox Series X Console with 1TB SSD, 4K@120fps gaming, Quick Resume, backward compatibility.',
                price=79999.00,
                original_price=89999.00,
                stock_quantity=18,
                category_id=4,
                brand='Microsoft',
                model='Series X',
                image_url='https://images.unsplash.com/photo-1621259182978-fbf93132d53d?w=400',
                is_featured=True,
                rating=4.8,
                review_count=654
            ),
            Product(
                name='Sony WH-1000XM5',
                description='Sony WH-1000XM5 wireless headphones with industry-leading noise cancellation, 30hr battery, Hi-Res audio.',
                price=34999.00,
                original_price=41999.00,
                stock_quantity=40,
                category_id=5,
                brand='Sony',
                model='WH-1000XM5',
                image_url='https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=400',
                is_featured=True,
                rating=4.8,
                review_count=1245
            ),
            Product(
                name='Apple AirPods Pro 2nd Gen',
                description='Apple AirPods Pro 2nd Generation with H2 chip, active noise cancellation, spatial audio, MagSafe charging.',
                price=28999.00,
                original_price=32999.00,
                stock_quantity=50,
                category_id=5,
                brand='Apple',
                model='AirPods Pro 2',
                image_url='https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=400',
                is_featured=True,
                rating=4.7,
                review_count=2156
            ),
            Product(
                name='Samsung Galaxy Buds2 Pro',
                description='Samsung Galaxy Buds2 Pro with 24-bit Hi-Fi sound, ANC, IPX7 water resistance, wireless charging.',
                price=18999.00,
                original_price=22999.00,
                stock_quantity=35,
                category_id=5,
                brand='Samsung',
                model='Buds2 Pro',
                image_url='https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400',
                is_featured=False,
                rating=4.5,
                review_count=567
            ),
            Product(
                name='Sony Alpha A7 IV',
                description='Sony Alpha A7 IV full-frame mirrorless camera, 33MP, 4K 60fps video, real-time eye AF, 5-axis stabilization.',
                price=249999.00,
                original_price=289999.00,
                stock_quantity=8,
                category_id=6,
                brand='Sony',
                model='A7 IV',
                image_url='https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400',
                is_featured=True,
                rating=4.9,
                review_count=234
            ),
            Product(
                name='Canon EOS R6 Mark II',
                description='Canon EOS R6 Mark II full-frame mirrorless, 24.2MP, 4K 60fps, 40fps burst, in-body stabilization.',
                price=269999.00,
                original_price=299999.00,
                stock_quantity=6,
                category_id=6,
                brand='Canon',
                model='EOS R6 Mark II',
                image_url='https://images.unsplash.com/photo-1510127034890-ba27508e9f1c?w=400',
                is_featured=False,
                rating=4.8,
                review_count=189
            ),
            Product(
                name='Amazon Echo Show 15',
                description='Amazon Echo Show 15 with 15.6" FHD display, Fire TV, Alexa, visual ID, streaming apps.',
                price=29999.00,
                original_price=34999.00,
                stock_quantity=20,
                category_id=7,
                brand='Amazon',
                model='Echo Show 15',
                image_url='https://images.unsplash.com/photo-1543512214-318c7553f230?w=400',
                is_featured=True,
                rating=4.5,
                review_count=456
            ),
            Product(
                name='Google Nest Hub Max',
                description='Google Nest Hub Max 10" smart display with Google Assistant, Nest Cam integration, stereo speakers.',
                price=22999.00,
                original_price=26999.00,
                stock_quantity=15,
                category_id=7,
                brand='Google',
                model='Nest Hub Max',
                image_url='https://images.unsplash.com/photo-1558002038-1055907df827?w=400',
                is_featured=False,
                rating=4.4,
                review_count=312
            ),
            Product(
                name='Anker 737 Power Bank',
                description='Anker 737 Power Bank 24,000mAh with 140W output, Smart Display, can charge laptop.',
                price=12999.00,
                original_price=15999.00,
                stock_quantity=60,
                category_id=8,
                brand='Anker',
                model='737 Power Bank',
                image_url='https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400',
                is_featured=True,
                rating=4.7,
                review_count=2345
            ),
            Product(
                name='Samsung 45W USB-C Charger',
                description='Samsung 45W USB-C fast charger with GaN technology, compatible with phones, tablets, laptops.',
                price=4999.00,
                original_price=5999.00,
                stock_quantity=100,
                category_id=8,
                brand='Samsung',
                model='45W Charger',
                image_url='https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=400',
                is_featured=False,
                rating=4.6,
                review_count=1567
            ),
            
            # Additional new products
            Product(
                name='ASUS ROG Strix G16',
                description='ASUS ROG Strix G16 gaming laptop with Intel Core i9, NVIDIA RTX 4080, 16GB RAM, 1TB SSD. Dominate your games with blazing-fast performance and stunning visuals on the 165Hz display.',
                price=219999.00,
                original_price=259999.00,
                stock_quantity=12,
                category_id=1,
                brand='ASUS',
                model='ROG Strix G16',
                image_url='https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?w=400',
                is_featured=True,
                rating=4.7,
                review_count=328
            ),
            Product(
                name='Lenovo ThinkPad X1 Carbon',
                description='Lenovo ThinkPad X1 Carbon Gen 11 with Intel Core i7, 32GB RAM, 1TB SSD, 14" OLED display. Ultra-lightweight business laptop built for professionals who demand reliability.',
                price=159999.00,
                original_price=189999.00,
                stock_quantity=18,
                category_id=1,
                brand='Lenovo',
                model='ThinkPad X1 Carbon',
                image_url='https://images.unsplash.com/photo-1588872657578-7efd1f155431?w=400',
                is_featured=False,
                rating=4.8,
                review_count=412
            ),
            Product(
                name='MSI Creator Z17',
                description='MSI Creator Z17 laptop with Intel Core i9, NVIDIA RTX 4080, 32GB RAM, 17" QHD+ touchscreen. The ultimate creative workstation for designers and digital artists.',
                price=269999.00,
                original_price=319999.00,
                stock_quantity=6,
                category_id=1,
                brand='MSI',
                model='Creator Z17',
                image_url='https://images.unsplash.com/photo-1611078489935-0cb964de46d6?w=400',
                is_featured=True,
                rating=4.9,
                review_count=156
            ),
            Product(
                name='iPhone 15',
                description='iPhone 15 with A16 Bionic chip, 128GB storage, Dynamic Island, 48MP camera system. The most affordable iPhone 15 delivers flagship features in a stunning design.',
                price=99999.00,
                original_price=119999.00,
                stock_quantity=35,
                category_id=2,
                brand='Apple',
                model='iPhone 15',
                image_url='https://images.unsplash.com/photo-1592750475338-f74a00c2312e?w=400',
                is_featured=True,
                rating=4.7,
                review_count=678
            ),
            Product(
                name='Samsung Galaxy Z Fold 5',
                description='Samsung Galaxy Z Fold 5 with 7.6" folding display, Snapdragon 8 Gen 2, 512GB storage. Transform your phone into a tablet for ultimate productivity and entertainment.',
                price=199999.00,
                original_price=229999.00,
                stock_quantity=10,
                category_id=2,
                brand='Samsung',
                model='Galaxy Z Fold 5',
                image_url='https://images.unsplash.com/photo-1628813989800-e842e2287c3f?w=400',
                is_featured=True,
                rating=4.6,
                review_count=234
            ),
            Product(
                name='OnePlus 12',
                description='OnePlus 12 with Snapdragon 8 Gen 3, 256GB storage, 50MP camera with Hasselblad tuning, 100W charging. Flagship performance at an unbeatable price point.',
                price=79999.00,
                original_price=99999.00,
                stock_quantity=22,
                category_id=2,
                brand='OnePlus',
                model='OnePlus 12',
                image_url='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400',
                is_featured=False,
                rating=4.7,
                review_count=445
            ),
            Product(
                name='Sony A95L 65" QD-OLED',
                description='Sony A95L 65" QD-OLED 4K Smart TV with Cognitive Processor XR, Google TV, Dolby Atmos, Acoustic Surface Audio+. Experience pictures and sound beyond reality.',
                price=249999.00,
                original_price=299999.00,
                stock_quantity=8,
                category_id=3,
                brand='Sony',
                model='A95L QD-OLED',
                image_url='https://images.unsplash.com/photo-1574359411659-15573a21844c?w=400',
                is_featured=True,
                rating=4.9,
                review_count=189
            ),
            Product(
                name='TCL C845 55" Mini LED',
                description='TCL C845 55" Mini LED 4K Smart TV with 576 zones, 144Hz refresh rate, Dolby Vision IQ, Google TV. Premium picture quality at an amazing value.',
                price=79999.00,
                original_price=99999.00,
                stock_quantity=15,
                category_id=3,
                brand='TCL',
                model='C845 Mini LED',
                image_url='https://images.unsplash.com/photo-1461151304267-38535e780c79?w=400',
                is_featured=False,
                rating=4.5,
                review_count=267
            ),
            Product(
                name='Nintendo Switch OLED',
                description='Nintendo Switch OLED with 7" OLED display, enhanced audio, 64GB storage. The ultimate portable gaming console with vibrant colors and immersive sound.',
                price=44999.00,
                original_price=49999.00,
                stock_quantity=25,
                category_id=4,
                brand='Nintendo',
                model='Switch OLED',
                image_url='https://images.unsplash.com/photo-1578303512597-81e6e155d6a3?w=400',
                is_featured=True,
                rating=4.8,
                review_count=1567
            ),
            Product(
                name='Steam Deck OLED',
                description='Valve Steam Deck OLED with 1TB SSD, 7" OLED display, 90Hz refresh rate. Handheld gaming PC with stunning visuals and all-day battery life.',
                price=79999.00,
                original_price=89999.00,
                stock_quantity=8,
                category_id=4,
                brand='Valve',
                model='Steam Deck OLED',
                image_url='https://images.unsplash.com/photo-1640955014216-75201016c829?w=400',
                is_featured=True,
                rating=4.9,
                review_count=823
            ),
            Product(
                name='Logitech G Pro X Gaming Headset',
                description='Logitech G Pro X Wireless gaming headset with Blue VO!CE technology, 50mm drivers, 20+ hour battery. Professional-grade audio for competitive gaming.',
                price=12999.00,
                original_price=15999.00,
                stock_quantity=45,
                category_id=4,
                brand='Logitech',
                model='G Pro X',
                image_url='https://images.unsplash.com/photo-1599669454699-248893623440?w=400',
                is_featured=False,
                rating=4.6,
                review_count=934
            ),
            Product(
                name='Bose QuietComfort Ultra',
                description='Bose QuietComfort Ultra headphones with spatial audio, CustomTune technology, 24hr battery. World-class noise cancellation meets immersive audio.',
                price=37999.00,
                original_price=44999.00,
                stock_quantity=30,
                category_id=5,
                brand='Bose',
                model='QuietComfort Ultra',
                image_url='https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400',
                is_featured=True,
                rating=4.8,
                review_count=567
            ),
            Product(
                name='Sennheiser Momentum 4',
                description='Sennheiser Momentum 4 Wireless with 60hr battery, adaptive noise cancellation, hi-res audio. Legendary sound quality meets modern design.',
                price=32999.00,
                original_price=39999.00,
                stock_quantity=25,
                category_id=5,
                brand='Sennheiser',
                model='Momentum 4',
                image_url='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
                is_featured=False,
                rating=4.7,
                review_count=389
            ),
            Product(
                name='Canon EOS R8',
                description='Canon EOS R8 full-frame mirrorless with 24.2MP, 4K 60fps, compact body. Perfect Entry into full-frame photography without compromise.',
                price=129999.00,
                original_price=159999.00,
                stock_quantity=10,
                category_id=6,
                brand='Canon',
                model='EOS R8',
                image_url='https://images.unsplash.com/photo-1502920917128-1aa500764c5c?w=400',
                is_featured=True,
                rating=4.7,
                review_count=145
            ),
            Product(
                name='GoPro Hero 12 Black',
                description='GoPro Hero 12 Black with 5.3K video, HyperSmooth 6.0, extended battery life, waterproof design. The ultimate action camera for adventurers.',
                price=44999.00,
                original_price=52999.00,
                stock_quantity=20,
                category_id=6,
                brand='GoPro',
                model='Hero 12 Black',
                image_url='https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400',
                is_featured=True,
                rating=4.8,
                review_count=678
            ),
            Product(
                name='Philips Hue Starter Kit',
                description='Philips Hue starter kit with 4 bulbs, Bridge, smart control. Transform your home with 16 million colors and voice control.',
                price=9999.00,
                original_price=12999.00,
                stock_quantity=50,
                category_id=7,
                brand='Philips',
                model='Hue Starter Kit',
                image_url='https://images.unsplash.com/photo-1558002038-1055907df827?w=400',
                is_featured=False,
                rating=4.6,
                review_count=1234
            ),
            Product(
                name='Ring Video Doorbell Pro',
                description='Ring Video Doorbell Pro with 2K resolution, HDR, dual-band WiFi, custom face plates. See who\'s at your door in crystal clear detail.',
                price=19999.00,
                original_price=24999.00,
                stock_quantity=25,
                category_id=7,
                brand='Ring',
                model='Video Doorbell Pro',
                image_url='https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400',
                is_featured=False,
                rating=4.5,
                review_count=892
            ),
            Product(
                name='Belkin Thunderbolt 4 Dock',
                description='Belkin Thunderbolt 4 Dock with 96W charging, 4K displays, 10 ports. The ultimate docking station for creative professionals.',
                price=34999.00,
                original_price=42999.00,
                stock_quantity=30,
                category_id=8,
                brand='Belkin',
                model='Thunderbolt 4 Dock',
                image_url='https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400',
                is_featured=True,
                rating=4.7,
                review_count=234
            ),
            Product(
                name='Samsung T7 Shield 2TB SSD',
                description='Samsung T7 Shield 2TB portable SSD with 1050MB/s, IP65 water/dust resistance, rubberized exterior. Rugged storage for professionals on the go.',
                price=22999.00,
                original_price=27999.00,
                stock_quantity=55,
                category_id=8,
                brand='Samsung',
                model='T7 Shield',
                image_url='https://images.unsplash.com/photo-1597872200969-2b65c56b6331?w=400',
                is_featured=True,
                rating=4.8,
                review_count=1567
            ),
            Product(
                name='Logitech MX Master 3S',
                description='Logitech MX Master 3S wireless mouse with 8K sensor, quiet clicks, MagSpeed scroll wheel. The ultimate productivity mouse for professionals.',
                price=9999.00,
                original_price=12999.00,
                stock_quantity=70,
                category_id=8,
                brand='Logitech',
                model='MX Master 3S',
                image_url='https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400',
                is_featured=True,
                rating=4.9,
                review_count=2456
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        print("✓ Products created successfully (39 total)")
        print("✓ Database initialized successfully!")

# Initialize when server starts
print("📦 Initializing database...")
init_database()

if __name__ == '__main__':
    print("🚀 Starting ElectroZone E-commerce API...")
    print("📡 API available at: http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/api/")
    app.run(debug=True, host='0.0.0.0', port=5000)