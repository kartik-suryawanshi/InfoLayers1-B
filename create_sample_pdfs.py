#!/usr/bin/env python3
"""
Create Sample PDFs for Menu Planning Challenge
Generates realistic PDF content for testing the system
"""

from pathlib import Path
import fitz  # PyMuPDF

def create_pdf_with_content(filename: str, title: str, content: str):
    """Create a PDF file with the given content."""
    doc = fitz.open()
    page = doc.new_page()
    
    # Add title
    page.insert_text((50, 50), title, fontsize=16)
    
    # Add content
    y_position = 100
    lines = content.split('\n')
    
    for line in lines:
        if line.strip():
            if line.startswith('#'):
                # Heading
                page.insert_text((50, y_position), line[1:].strip(), fontsize=14)
                y_position += 30
            else:
                # Regular text
                page.insert_text((50, y_position), line, fontsize=12)
                y_position += 20
        
        if y_position > 750:  # New page if needed
            page = doc.new_page()
            y_position = 50
    
    # Save PDF
    pdf_path = Path("documents") / filename
    pdf_path.parent.mkdir(exist_ok=True)
    doc.save(str(pdf_path))
    doc.close()
    print(f"Created: {filename}")

def create_menu_planning_pdfs():
    """Create sample PDF files for menu planning challenge."""
    
    # Breakfast Ideas
    breakfast_content = """# Breakfast Ideas

# Continental Breakfast
Fresh croissants and pastries served with butter and jam
Assorted fresh fruits and berries
Greek yogurt with honey and granola
Freshly squeezed orange juice
Coffee and tea selection

# Vegetarian Breakfast Bowl
Quinoa cooked in vegetable broth
Sautéed spinach and mushrooms
Avocado slices and cherry tomatoes
Poached eggs (optional)
Fresh herbs and microgreens
Light vinaigrette dressing

# Gluten-Free Breakfast Options
Buckwheat pancakes with maple syrup
Chia seed pudding with almond milk
Fresh fruit salad with coconut flakes
Almond butter on rice cakes
Herbal tea and fresh juice

# Healthy Start
Oatmeal with fresh berries and nuts
Whole grain toast with avocado
Smoothie bowl with granola
Green tea and fresh juice
Mixed nuts and dried fruits"""

    # Dinner Ideas - Mains 1
    mains1_content = """# Dinner Ideas - Mains 1

# Vegetarian Lasagna
Layers of fresh pasta sheets
Ricotta cheese and spinach filling
Marinara sauce with fresh herbs
Mozzarella and parmesan cheese
Baked until golden and bubbly

# Ratatouille
Traditional Provençal vegetable stew
Eggplant, zucchini, and bell peppers
Fresh tomatoes and onions
Herbs de Provence seasoning
Served with crusty bread

# Mushroom Risotto
Arborio rice cooked to perfection
Mixed wild mushrooms
Vegetable broth and white wine
Parmesan cheese and fresh herbs
Creamy and comforting texture

# Stuffed Bell Peppers
Bell peppers filled with quinoa
Black beans and corn mixture
Mexican spices and seasonings
Topped with melted cheese
Served with fresh salsa"""

    # Dinner Ideas - Mains 2
    mains2_content = """# Dinner Ideas - Mains 2

# Vegetable Curry
Mixed vegetables in aromatic curry sauce
Coconut milk and fresh spices
Basmati rice and naan bread
Fresh cilantro and lime garnish
Mild to spicy heat levels

# Falafel Platter
Crispy chickpea fritters
Fresh pita bread and hummus
Tahini sauce and pickled vegetables
Mixed green salad
Mediterranean flavors

# Pasta Primavera
Fresh seasonal vegetables
Al dente pasta of choice
Light cream sauce with herbs
Parmesan cheese garnish
Quick and delicious preparation

# Vegetable Stir Fry
Crisp vegetables in wok
Soy sauce and ginger marinade
Brown rice or quinoa base
Sesame seeds and green onions
Asian-inspired flavors"""

    # Dinner Ideas - Mains 3
    mains3_content = """# Dinner Ideas - Mains 3

# Stuffed Portobello Mushrooms
Large portobello caps
Quinoa and vegetable stuffing
Balsamic glaze and herbs
Melted cheese topping
Elegant presentation

# Vegetable Paella
Saffron-infused rice dish
Mixed vegetables and legumes
Spanish paprika and herbs
Lemon wedges for garnish
Authentic Spanish flavors

# Lentil Shepherd's Pie
Mashed potato topping
Lentil and vegetable filling
Herbs and seasonings
Golden brown crust
Comfort food classic

# Vegetable Wellington
Puff pastry wrapped vegetables
Mushroom and spinach filling
Herb and garlic seasoning
Golden flaky crust
Elegant main course"""

    # Dinner Ideas - Sides 1
    sides1_content = """# Dinner Ideas - Sides 1

# Roasted Vegetables
Assorted seasonal vegetables
Olive oil and herb seasoning
Caramelized edges and tender centers
Fresh herbs for garnish
Colorful and nutritious

# Quinoa Salad
Cooked quinoa with fresh vegetables
Lemon vinaigrette dressing
Fresh herbs and feta cheese
Light and refreshing side
Protein-rich option

# Garlic Mashed Potatoes
Creamy mashed potatoes
Roasted garlic and butter
Fresh herbs and seasoning
Smooth and comforting
Classic side dish

# Grilled Asparagus
Fresh asparagus spears
Olive oil and lemon seasoning
Parmesan cheese shavings
Tender and flavorful
Spring vegetable favorite"""

    # Dinner Ideas - Sides 2
    sides2_content = """# Dinner Ideas - Sides 2

# Mediterranean Salad
Mixed greens and vegetables
Olive oil and balsamic dressing
Feta cheese and olives
Fresh herbs and spices
Light and refreshing

# Roasted Sweet Potatoes
Sweet potato wedges
Cinnamon and maple seasoning
Crispy edges and tender centers
Nutritious and delicious
Fall favorite

# Steamed Broccoli
Fresh broccoli florets
Light butter and lemon
Al dente texture
Simple and healthy
Classic green vegetable

# Couscous Pilaf
Fluffy couscous with vegetables
Herbs and spices
Light broth cooking
Flavorful and quick
Mediterranean side dish"""

    # Dinner Ideas - Sides 3
    sides3_content = """# Dinner Ideas - Sides 3

# Gluten-Free Options

# Cauliflower Rice
Riced cauliflower
Light seasoning and herbs
Low-carb alternative
Quick and healthy
Versatile side dish

# Zucchini Noodles
Spiralized zucchini
Light sauce and herbs
Low-carb pasta alternative
Fresh and crisp
Healthy noodle option

# Roasted Brussels Sprouts
Halved Brussels sprouts
Balsamic glaze and nuts
Caramelized edges
Nutritious and flavorful
Fall vegetable favorite

# Quinoa Pilaf
Cooked quinoa with vegetables
Herbs and light seasoning
Protein-rich side dish
Gluten-free grain option
Healthy and satisfying"""

    # Dinner Ideas - Sides 4
    sides4_content = """# Dinner Ideas - Sides 4

# Buffet-Style Sides

# Mixed Green Salad
Fresh mixed greens
Assorted vegetables
Light vinaigrette
Croutons and nuts
Classic salad option

# Roasted Root Vegetables
Carrots, parsnips, and turnips
Herb and olive oil seasoning
Caramelized sweetness
Colorful presentation
Fall vegetable medley

# Wild Rice Blend
Mixed wild rice varieties
Vegetable broth cooking
Herbs and seasoning
Nutty and flavorful
Elegant side dish

# Steamed Green Beans
Fresh green beans
Light butter and herbs
Crisp-tender texture
Simple and healthy
Classic vegetable side"""

    # Lunch Ideas
    lunch_content = """# Lunch Ideas

# Vegetarian Wraps
Fresh tortillas with vegetables
Hummus and avocado spread
Mixed greens and sprouts
Light and portable
Perfect for lunch

# Buddha Bowl
Quinoa or rice base
Assorted vegetables
Protein-rich legumes
Light dressing
Balanced meal option

# Mediterranean Platter
Hummus and pita bread
Fresh vegetables and olives
Feta cheese and nuts
Light and satisfying
Mediterranean flavors

# Vegetable Soup
Fresh seasonal vegetables
Light broth base
Herbs and seasoning
Warm and comforting
Healthy lunch option"""

    # Create all PDFs
    pdfs = [
        ("Breakfast Ideas.pdf", "Breakfast Ideas", breakfast_content),
        ("Dinner Ideas - Mains_1.pdf", "Dinner Ideas - Mains 1", mains1_content),
        ("Dinner Ideas - Mains_2.pdf", "Dinner Ideas - Mains 2", mains2_content),
        ("Dinner Ideas - Mains_3.pdf", "Dinner Ideas - Mains 3", mains3_content),
        ("Dinner Ideas - Sides_1.pdf", "Dinner Ideas - Sides 1", sides1_content),
        ("Dinner Ideas - Sides_2.pdf", "Dinner Ideas - Sides 2", sides2_content),
        ("Dinner Ideas - Sides_3.pdf", "Dinner Ideas - Sides 3", sides3_content),
        ("Dinner Ideas - Sides_4.pdf", "Dinner Ideas - Sides 4", sides4_content),
        ("Lunch Ideas.pdf", "Lunch Ideas", lunch_content)
    ]
    
    for filename, title, content in pdfs:
        create_pdf_with_content(filename, title, content)

if __name__ == "__main__":
    create_menu_planning_pdfs()
    print("✅ All sample PDFs created successfully!") 