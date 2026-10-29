-- ====================================================================
-- Quick Mart Retail Store Management & POS System
-- Relational Database Schema & Seed Data Script
-- Target Engine: SQLite 3 (Compatible with PostgreSQL / MySQL)
-- ====================================================================

PRAGMA foreign_keys = ON;

-- --------------------------------------------------------------------
-- Table Structure: users
-- --------------------------------------------------------------------
CREATE TABLE users (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	role VARCHAR(50) NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_users_email ON users (email);

-- Seed Data: users (2 records)
INSERT INTO users ("id", "name", "email", "password_hash", "role", "created_at") VALUES (1, 'Store Admin', 'admin@quickmart.com', 'scrypt:32768:8:1$PKE9000jZBwvtC5x$cc796ae3961f29c920115abdf25ef1b5048575ea5cbc1281c9e48f9a41cc09d3ab549adbcc623cc96ee6b281ca91ba27245dcb122d7d8758c8e9c5a8f45c5c76', 'admin', '2026-10-19 05:42:10.992859');
INSERT INTO users ("id", "name", "email", "password_hash", "role", "created_at") VALUES (2, 'Priya Sharma', 'cashier@quickmart.com', 'scrypt:32768:8:1$f6SQtPFtkFFva2wp$f29a4e46e1654518f8f3a01a405db827126412b71aad2848f9798b4f473ad206f1608248831b22dd7e5d6cf7ba65bd2bf2485a530b7ba0aca802d71c9a815b8f', 'cashier', '2026-10-19 05:42:10.992863');

-- --------------------------------------------------------------------
-- Table Structure: suppliers
-- --------------------------------------------------------------------
CREATE TABLE suppliers (
	id INTEGER NOT NULL, 
	name VARCHAR(150) NOT NULL, 
	contact_person VARCHAR(100), 
	phone VARCHAR(25), 
	email VARCHAR(120), 
	address TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);

-- Seed Data: suppliers (3 records)
INSERT INTO suppliers ("id", "name", "contact_person", "phone", "email", "address", "created_at") VALUES (1, 'FarmFresh Organics & Agro', 'Rajesh Sharma', '+91 98765 43210', 'rajesh@farmfreshagro.in', 'Gala 14, APMC Fruit & Veg Wholesale Market, Vashi, Navi Mumbai', '2026-10-19 05:42:10.989275');
INSERT INTO suppliers ("id", "name", "contact_person", "phone", "email", "address", "created_at") VALUES (2, 'Apex FMCG & Consumer Goods', 'Sunita Patel', '+91 91234 56789', 'orders@apexfmcg.com', 'Unit 4B, MIDC Central Road, Andheri East, Mumbai', '2026-10-19 05:42:10.989280');
INSERT INTO suppliers ("id", "name", "contact_person", "phone", "email", "address", "created_at") VALUES (3, 'Metro Tech & Home Essentials', 'Amit Verma', '+91 99887 76655', 'sales@metrotechsupplies.in', 'Plot 88, Electronic Zone, Hinjewadi Phase 1, Pune', '2026-10-19 05:42:10.989282');

-- --------------------------------------------------------------------
-- Table Structure: products
-- --------------------------------------------------------------------
CREATE TABLE products (
	id INTEGER NOT NULL, 
	name VARCHAR(150) NOT NULL, 
	category VARCHAR(50) NOT NULL, 
	price FLOAT NOT NULL, 
	stock_quantity INTEGER NOT NULL, 
	supplier_id INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(supplier_id) REFERENCES suppliers (id) ON DELETE SET NULL
);

CREATE INDEX ix_products_category ON products (category);
CREATE INDEX ix_products_name ON products (name);

-- Seed Data: products (86 records)
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (1, 'Farm Fresh Organic Broccoli', 'Vegetables', 85.0, 4, 1, '2026-10-19 05:42:10.995254');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (2, 'Ratnagiri Alphonso Mangoes (1 Dozen)', 'Fruits', 650.0, 2, 1, '2026-10-19 05:42:10.995257');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (3, 'Cast Iron Pre-Seasoned Skillet 10-inch', 'Kitchen', 1299.0, 8, 3, '2026-10-19 05:42:10.995258');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (4, 'Royal Basmati Rice Aged 5kg', 'Grocery', 420.0, 15, 2, '2026-10-19 05:42:10.995259');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (5, 'Cold Pressed Virgin Coconut Oil 1L', 'Grocery', 275.0, 22, 2, '2026-10-19 05:42:10.995260');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (6, 'Rechargeable Wireless Mouse', 'Electronics', 549.0, 18, 3, '2026-10-19 05:42:10.995262');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (7, 'Natural Aloe & Tea Tree Hand Wash 500ml', 'Toiletries', 140.0, 26, 2, '2026-10-19 05:42:10.995263');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (8, 'Handcrafted Scented Soy Candle', 'Decor', 350.0, 11, 3, '2026-10-19 05:42:10.995264');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (9, 'Crisp Hydroponic Tomatoes 1kg', 'Vegetables', 45.0, 80, 1, '2026-10-19 05:42:10.995265');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (10, 'Shimla Royal Gala Apples 1kg', 'Fruits', 180.0, 64, 1, '2026-10-19 05:42:10.995267');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (11, 'Chakki Fresh Whole Wheat Atta 10kg', 'Grocery', 410.0, 55, 2, '2026-10-19 05:42:10.995268');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (12, 'Braided Nylon Type-C Fast Cable', 'Electronics', 249.0, 90, 3, '2026-10-19 05:42:10.995269');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (13, 'Herbal Moisturizing Body Lotion 400ml', 'Toiletries', 260.0, 48, 2, '2026-10-19 05:42:10.995270');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (14, 'Minimalist Ceramic Succulent Planter', 'Decor', 299.0, 37, 3, '2026-10-19 05:42:10.995271');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (15, 'Stainless Steel Chef Knife 8-inch', 'Kitchen', 599.0, 42, 3, '2026-10-19 05:42:10.995273');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (16, 'Hydroponic Baby Spinach 250g', 'Vegetables', 40.0, 50, 1, '2026-10-19 05:42:10.995274');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (17, 'Premium Imported Kiwi (3 Pack)', 'Fruits', 120.0, 34, 1, '2026-10-19 05:42:10.995275');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (21, 'Fresh English Cucumber 500g', 'Vegetables', 30.0, 45, 1, '2026-10-19 06:09:59.699510');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (22, 'Red Bell Peppers 500g', 'Vegetables', 75.0, 18, 1, '2026-10-19 06:09:59.702767');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (23, 'Yellow Sweet Corn (Pack of 2)', 'Vegetables', 40.0, 25, 1, '2026-10-19 06:09:59.703533');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (24, 'Button Mushrooms 200g', 'Vegetables', 60.0, 8, 1, '2026-10-19 06:09:59.704200');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (25, 'Organic Baby Carrots 500g', 'Vegetables', 55.0, 35, 1, '2026-10-19 06:09:59.704870');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (26, 'Purple Cabbage 500g', 'Vegetables', 45.0, 22, 1, '2026-10-19 06:09:59.705499');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (27, 'Green Zucchini 500g', 'Vegetables', 65.0, 9, 1, '2026-10-19 06:09:59.706097');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (28, 'Fresh Coriander Bunch', 'Vegetables', 15.0, 60, 1, '2026-10-19 06:09:59.706717');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (29, 'Farm Fresh Cauliflower', 'Vegetables', 35.0, 40, 1, '2026-10-19 06:09:59.707357');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (30, 'Nagpur Mandarin Oranges 1kg', 'Fruits', 90.0, 55, 1, '2026-10-19 06:09:59.709520');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (31, 'Robusta Golden Bananas 1kg', 'Fruits', 50.0, 70, 1, '2026-10-19 06:09:59.710526');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (32, 'Seedless Black Grapes 500g', 'Fruits', 85.0, 24, 1, '2026-10-19 06:09:59.711398');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (33, 'Fresh Pomegranate 1kg', 'Fruits', 160.0, 15, 1, '2026-10-19 06:09:59.712131');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (34, 'Imported Green Dragonfruit', 'Fruits', 140.0, 8, 1, '2026-10-19 06:09:59.712813');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (35, 'Sweet Imported Blueberries 125g', 'Fruits', 220.0, 7, 1, '2026-10-19 06:09:59.713420');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (36, 'Sun Melon 1kg', 'Fruits', 60.0, 30, 1, '2026-10-19 06:09:59.714071');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (37, 'Ripe Hass Avocado (Pack of 2)', 'Fruits', 210.0, 12, 1, '2026-10-19 06:09:59.714692');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (38, 'Fresh Papaya 1kg', 'Fruits', 45.0, 40, 1, '2026-10-19 06:09:59.715296');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (39, 'Organic Toor Dal 1kg', 'Grocery', 165.0, 45, 2, '2026-10-19 06:09:59.717499');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (40, 'Premium Tata Salt 1kg', 'Grocery', 28.0, 120, 2, '2026-10-19 06:09:59.718156');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (41, 'Sulphur Free Refined Sugar 1kg', 'Grocery', 52.0, 85, 2, '2026-10-19 06:09:59.718763');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (42, 'Cold Pressed Mustard Oil 1L', 'Grocery', 195.0, 28, 2, '2026-10-19 06:09:59.719370');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (43, 'Pure Cow Ghee 500ml', 'Grocery', 380.0, 9, 2, '2026-10-19 06:09:59.720022');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (44, 'Organic Rolled Oats 1kg', 'Grocery', 190.0, 32, 2, '2026-10-19 06:09:59.720645');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (45, 'Roasted California Almonds 500g', 'Grocery', 490.0, 7, 2, '2026-10-19 06:09:59.721237');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (46, 'Premium Cashews Whole 500g', 'Grocery', 520.0, 14, 2, '2026-10-19 06:09:59.721828');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (47, 'Masala Tea Leaves 500g', 'Grocery', 230.0, 40, 2, '2026-10-19 06:09:59.722422');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (48, 'Instant Arabica Coffee 100g', 'Grocery', 285.0, 18, 2, '2026-10-19 06:09:59.723030');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (49, 'Bluetooth 5.3 Earbuds with Mic', 'Electronics', 1299.0, 12, 3, '2026-10-19 06:09:59.724639');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (50, '20W USB-C Fast Wall Charger', 'Electronics', 499.0, 35, 3, '2026-10-19 06:09:59.725237');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (51, '10000mAh Slim Power Bank', 'Electronics', 899.0, 8, 3, '2026-10-19 06:09:59.725951');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (52, 'Multi-Plug Surge Protector Extension', 'Electronics', 599.0, 25, 3, '2026-10-19 06:09:59.726824');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (53, 'High-Speed 64GB USB 3.0 Flash Drive', 'Electronics', 380.0, 40, 3, '2026-10-19 06:09:59.727689');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (54, 'Portable Clip-on Desk Fan (USB)', 'Electronics', 650.0, 16, 3, '2026-10-19 06:09:59.728494');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (55, 'Rechargeable LED Emergency Torch', 'Electronics', 320.0, 50, 3, '2026-10-19 06:09:59.729176');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (56, 'Ergonomic Laptop Riser Stand', 'Electronics', 799.0, 6, 3, '2026-10-19 06:09:59.729813');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (57, 'Smart Wi-Fi 9W RGB LED Bulb', 'Electronics', 449.0, 28, 3, '2026-10-19 06:09:59.731433');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (58, 'AAA Alkaline Batteries (Pack of 8)', 'Electronics', 199.0, 65, 3, '2026-10-19 06:09:59.732135');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (59, 'Refreshing Citrus Shower Gel 300ml', 'Toiletries', 199.0, 32, 2, '2026-10-19 06:09:59.733823');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (60, 'Charcoal Deep Clean Face Wash 150ml', 'Toiletries', 175.0, 40, 2, '2026-10-19 06:09:59.734436');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (61, 'Anti-Dandruff Keratin Shampoo 350ml', 'Toiletries', 280.0, 15, 2, '2026-10-19 06:09:59.735086');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (62, 'Organic Bamboo Toothbrush (Pack of 4)', 'Toiletries', 149.0, 55, 2, '2026-10-19 06:09:59.735685');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (63, 'Complete Care Herbal Toothpaste 150g', 'Toiletries', 95.0, 80, 2, '2026-10-19 06:09:59.736268');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (64, 'Gentle Baby Wet Wipes (Pack of 72)', 'Toiletries', 120.0, 60, 2, '2026-10-19 06:09:59.736891');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (65, 'Soft 3-Ply Bathroom Tissue Rolls (Pack of 6)', 'Toiletries', 210.0, 22, 2, '2026-10-19 06:09:59.737513');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (66, 'Ultra Nourishing Lip Balm SPF 15', 'Toiletries', 125.0, 8, 2, '2026-10-19 06:09:59.738111');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (67, 'Hand Sanitizer Gel 500ml Pump', 'Toiletries', 150.0, 45, 2, '2026-10-19 06:09:59.738725');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (68, 'Luxury Fragrance Deodorant Body Spray', 'Toiletries', 220.0, 9, 2, '2026-10-19 06:09:59.739354');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (69, 'Warm White Fairy Curtain Lights 3M', 'Decor', 399.0, 24, 3, '2026-10-19 06:09:59.740976');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (70, 'Bohemian Macrame Wall Hanging', 'Decor', 549.0, 7, 3, '2026-10-19 06:09:59.741577');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (71, 'Nordic Geometric Ceramic Flower Vase', 'Decor', 480.0, 15, 3, '2026-10-19 06:09:59.742159');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (72, 'Textured Cotton Cushion Cover (Pack of 2)', 'Decor', 340.0, 30, 3, '2026-10-19 06:09:59.742779');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (73, 'Wooden Essential Oil Reed Diffuser', 'Decor', 420.0, 8, 3, '2026-10-19 06:09:59.743640');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (74, 'Vintage Antique Tabletop Clock', 'Decor', 699.0, 5, 3, '2026-10-19 06:09:59.744612');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (75, 'Woven Jute Floor Mat / Rug 60x90cm', 'Decor', 599.0, 18, 3, '2026-10-19 06:09:59.745358');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (76, 'Golden Brass Tea Light Candle Holders', 'Decor', 290.0, 42, 3, '2026-10-19 06:09:59.745985');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (77, 'Wooden Motivational Wall Art Frame', 'Decor', 250.0, 35, 3, '2026-10-19 06:09:59.746571');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (78, 'Ceramic Incense Burner with Backflow Cones', 'Decor', 380.0, 20, 3, '2026-10-19 06:09:59.747207');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (79, 'Non-Stick 3-Piece Cookware Set', 'Kitchen', 1899.0, 6, 3, '2026-10-19 06:09:59.748866');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (80, 'Borosilicate Glass Food Storage Containers (3 Pack)', 'Kitchen', 749.0, 16, 3, '2026-10-19 06:09:59.749470');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (81, 'Heavy Duty Garlic Press Crusher', 'Kitchen', 249.0, 30, 3, '2026-10-19 06:09:59.750048');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (82, 'Heat Resistant Silicone Spatula Set (4 Pcs)', 'Kitchen', 299.0, 50, 3, '2026-10-19 06:09:59.750663');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (83, 'Stainless Steel Oil Dispenser Bottle 1L', 'Kitchen', 320.0, 35, 3, '2026-10-19 06:09:59.751271');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (84, 'Digital Kitchen Food Weighing Scale', 'Kitchen', 450.0, 14, 3, '2026-10-19 06:09:59.751851');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (85, 'Bamboo Kitchen Chopping Board Large', 'Kitchen', 399.0, 28, 3, '2026-10-19 06:09:59.752459');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (86, 'Stainless Steel Insulated Water Bottle 750ml', 'Kitchen', 480.0, 40, 3, '2026-10-19 06:09:59.753067');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (87, 'Manual Hand Pull Vegetable Chopper', 'Kitchen', 275.0, 45, 3, '2026-10-19 06:09:59.753639');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (88, '6-Piece Ceramic Coffee Mug Set', 'Kitchen', 540.0, 9, 3, '2026-10-19 06:09:59.754121');
INSERT INTO products ("id", "name", "category", "price", "stock_quantity", "supplier_id", "created_at") VALUES (89, 'Test Crisp Honey Apples', 'Fruits', 99.5, 45, NULL, '2026-10-19 06:10:36.176363');

-- --------------------------------------------------------------------
-- Table Structure: bills
-- --------------------------------------------------------------------
CREATE TABLE bills (
	id INTEGER NOT NULL, 
	bill_number VARCHAR(50) NOT NULL, 
	customer_name VARCHAR(100) NOT NULL, 
	customer_mobile VARCHAR(25) NOT NULL, 
	subtotal FLOAT NOT NULL, 
	sgst FLOAT NOT NULL, 
	cgst FLOAT NOT NULL, 
	total_amount FLOAT NOT NULL, 
	payment_method VARCHAR(30) NOT NULL, 
	timestamp DATETIME, 
	PRIMARY KEY (id)
);

CREATE INDEX ix_bills_timestamp ON bills (timestamp);
CREATE UNIQUE INDEX ix_bills_bill_number ON bills (bill_number);

-- Seed Data: bills (15 records)
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (1, 'QM-202610-1001', 'Rohan Mehta', '+91 98201 11223', 1668.0, 150.12, 150.12, 1968.24, 'UPI', '2026-10-10 03:32:10.996642');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (2, 'QM-202610-1002', 'Ananya Iyer', '+91 97112 33445', 1847.0, 166.23, 166.23, 2179.46, 'Cash', '2026-10-10 21:26:10.996642');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (3, 'QM-202610-1003', 'Vikram Singhania', '+91 99304 55667', 1340.0, 120.6, 120.6, 1581.2, 'UPI', '2026-10-11 22:06:10.996642');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (4, 'QM-202610-1004', 'Kavita Rao', '+91 98450 77889', 2268.0, 204.12, 204.12, 2676.24, 'Card', '2026-10-12 20:59:10.996642');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (5, 'QM-202610-1005', 'Aditya Kapoor', '+91 99200 99881', 1540.0, 138.6, 138.6, 1817.2, 'Card', '2026-10-14 03:55:10.996642');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (6, 'QM-202610-1006', 'Sneha Joshi', '+91 98190 22334', 3783.0, 340.47, 340.47, 4463.94, 'UPI', '2026-10-15 04:10:10.996642');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (7, 'QM-202610-1007', 'Arjun Deshmukh', '+91 98670 44556', 3121.0, 280.89, 280.89, 3682.78, 'Cash', '2026-10-16 03:11:10.996642');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (8, 'QM-202610-1008', 'Meera Nair', '+91 97420 66778', 888.0, 79.92, 79.92, 1047.84, 'Card', '2026-10-16 20:22:10.996642');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (9, 'QM-202610-1009', 'Rahul Bansal', '+91 98880 88990', 565.0, 50.85, 50.85, 666.7, 'Card', '2026-10-18 03:24:10.996642');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (10, 'QM-202610-1010', 'Tanvi Kulkarni', '+91 98230 11335', 1195.0, 107.55, 107.55, 1410.1, 'UPI', '2026-10-18 21:19:10.996642');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (11, 'QM-202610-0011', 'Test Customer', '+91 99999 88888', 220.0, 19.8, 19.8, 259.6, 'UPI', '2026-10-19 05:44:30.514116');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (12, 'QM-202610-0012', 'vedany', '7666398344', 2468.5, 222.16, 222.16, 2912.82, 'Cash', '2026-10-19 05:50:11.936396');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (13, 'QM-202610-0013', 'Test Customer', '+91 99999 88888', 220.0, 19.8, 19.8, 259.6, 'UPI', '2026-10-19 06:04:20.104622');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (14, 'QM-202610-0014', 'Test Customer', '+91 99999 88888', 220.0, 19.8, 19.8, 259.6, 'UPI', '2026-10-19 06:10:36.238296');
INSERT INTO bills ("id", "bill_number", "customer_name", "customer_mobile", "subtotal", "sgst", "cgst", "total_amount", "payment_method", "timestamp") VALUES (15, 'QM-202610-0015', 'Test Customer', '+91 99999 88888', 170.0, 15.3, 15.3, 200.6, 'UPI', '2026-10-26 20:26:47.959674');

-- --------------------------------------------------------------------
-- Table Structure: bill_items
-- --------------------------------------------------------------------
CREATE TABLE bill_items (
	id INTEGER NOT NULL, 
	bill_id INTEGER NOT NULL, 
	product_id INTEGER, 
	product_name VARCHAR(150) NOT NULL, 
	quantity INTEGER NOT NULL, 
	price_at_sale FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(bill_id) REFERENCES bills (id) ON DELETE CASCADE, 
	FOREIGN KEY(product_id) REFERENCES products (id) ON DELETE SET NULL
);

-- Seed Data: bill_items (41 records)
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (1, 1, 12, 'Braided Nylon Type-C Fast Cable', 2, 249.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (2, 1, 2, 'Ratnagiri Alphonso Mangoes (1 Dozen)', 1, 650.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (3, 1, 13, 'Herbal Moisturizing Body Lotion 400ml', 2, 260.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (4, 2, 8, 'Handcrafted Scented Soy Candle', 2, 350.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (5, 2, 1, 'Farm Fresh Organic Broccoli', 2, 85.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (6, 2, 16, 'Hydroponic Baby Spinach 250g', 2, 40.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (7, 2, 14, 'Minimalist Ceramic Succulent Planter', 3, 299.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (8, 3, 11, 'Chakki Fresh Whole Wheat Atta 10kg', 2, 410.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (9, 3, 13, 'Herbal Moisturizing Body Lotion 400ml', 2, 260.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (10, 4, 4, 'Royal Basmati Rice Aged 5kg', 3, 420.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (11, 4, 11, 'Chakki Fresh Whole Wheat Atta 10kg', 1, 410.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (12, 4, 14, 'Minimalist Ceramic Succulent Planter', 2, 299.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (13, 5, 8, 'Handcrafted Scented Soy Candle', 2, 350.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (14, 5, 4, 'Royal Basmati Rice Aged 5kg', 2, 420.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (15, 6, 17, 'Premium Imported Kiwi (3 Pack)', 3, 120.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (16, 6, 5, 'Cold Pressed Virgin Coconut Oil 1L', 3, 275.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (17, 6, 3, 'Cast Iron Pre-Seasoned Skillet 10-inch', 2, 1299.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (18, 7, 11, 'Chakki Fresh Whole Wheat Atta 10kg', 2, 410.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (19, 7, 12, 'Braided Nylon Type-C Fast Cable', 3, 249.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (20, 7, 3, 'Cast Iron Pre-Seasoned Skillet 10-inch', 1, 1299.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (21, 7, 1, 'Farm Fresh Organic Broccoli', 3, 85.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (22, 8, 16, 'Hydroponic Baby Spinach 250g', 1, 40.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (23, 8, 12, 'Braided Nylon Type-C Fast Cable', 2, 249.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (24, 8, 8, 'Handcrafted Scented Soy Candle', 1, 350.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (25, 9, 1, 'Farm Fresh Organic Broccoli', 2, 85.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (26, 9, 17, 'Premium Imported Kiwi (3 Pack)', 1, 120.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (27, 9, 5, 'Cold Pressed Virgin Coconut Oil 1L', 1, 275.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (28, 10, 13, 'Herbal Moisturizing Body Lotion 400ml', 1, 260.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (29, 10, 10, 'Shimla Royal Gala Apples 1kg', 3, 180.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (30, 10, 8, 'Handcrafted Scented Soy Candle', 1, 350.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (31, 10, 9, 'Crisp Hydroponic Tomatoes 1kg', 1, 45.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (32, 11, NULL, 'Test Crisp Honey Apples Premium', 2, 110.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (33, 12, 8, 'Handcrafted Scented Soy Candle', 1, 350.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (34, 12, 14, 'Minimalist Ceramic Succulent Planter', 1, 299.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (35, 12, 17, 'Premium Imported Kiwi (3 Pack)', 2, 120.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (36, 12, 2, 'Ratnagiri Alphonso Mangoes (1 Dozen)', 2, 650.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (37, 12, 10, 'Shimla Royal Gala Apples 1kg', 1, 180.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (38, 12, NULL, 'Test Crisp Honey Apples', 1, 99.5);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (39, 13, NULL, 'Test Crisp Honey Apples Premium', 2, 110.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (40, 14, NULL, 'Test Crisp Honey Apples Premium', 2, 110.0);
INSERT INTO bill_items ("id", "bill_id", "product_id", "product_name", "quantity", "price_at_sale") VALUES (41, 15, 1, 'Farm Fresh Organic Broccoli', 2, 85.0);

