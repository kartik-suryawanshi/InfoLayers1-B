#!/usr/bin/env python3
"""
Create Real JSON Files with Actual Content
Generates JSON files with proper dish names and content for testing
"""

import json
from pathlib import Path

def create_menu_json_files():
    """Create JSON files with real menu content."""
    
    json_dir = Path("input_json_dir")
    json_dir.mkdir(exist_ok=True)
    
    # Clear existing JSON files
    for file in json_dir.glob("*.json"):
        file.unlink()
    
    # Breakfast Ideas
    breakfast_json = {
        "filename": "Breakfast Ideas.pdf",
        "sections": [
            {
                "page_number": 1,
                "heading": "Continental Breakfast",
                "text": "Fresh croissants and pastries served with butter and jam. Assorted fresh fruits and berries. Greek yogurt with honey and granola. Freshly squeezed orange juice. Coffee and tea selection."
            },
            {
                "page_number": 1,
                "heading": "Vegetarian Breakfast Bowl",
                "text": "Quinoa cooked in vegetable broth. Sautéed spinach and mushrooms. Avocado slices and cherry tomatoes. Poached eggs (optional). Fresh herbs and microgreens. Light vinaigrette dressing."
            },
            {
                "page_number": 1,
                "heading": "Gluten-Free Breakfast Options",
                "text": "Buckwheat pancakes with maple syrup. Chia seed pudding with almond milk. Fresh fruit salad with coconut flakes. Almond butter on rice cakes. Herbal tea and fresh juice."
            },
            {
                "page_number": 1,
                "heading": "Healthy Start",
                "text": "Oatmeal with fresh berries and nuts. Whole grain toast with avocado. Smoothie bowl with granola. Green tea and fresh juice. Mixed nuts and dried fruits."
            }
        ]
    }
    
    # Dinner Ideas - Mains 1
    mains1_json = {
        "filename": "Dinner Ideas - Mains_1.pdf",
        "sections": [
            {
                "page_number": 1,
                "heading": "Vegetarian Lasagna",
                "text": "Layers of fresh pasta sheets. Ricotta cheese and spinach filling. Marinara sauce with fresh herbs. Mozzarella and parmesan cheese. Baked until golden and bubbly."
            },
            {
                "page_number": 1,
                "heading": "Ratatouille",
                "text": "Traditional Provençal vegetable stew. Eggplant, zucchini, and bell peppers. Fresh tomatoes and onions. Herbs de Provence seasoning. Served with crusty bread."
            },
            {
                "page_number": 1,
                "heading": "Mushroom Risotto",
                "text": "Arborio rice cooked to perfection. Mixed wild mushrooms. Vegetable broth and white wine. Parmesan cheese and fresh herbs. Creamy and comforting texture."
            },
            {
                "page_number": 1,
                "heading": "Stuffed Bell Peppers",
                "text": "Bell peppers filled with quinoa. Black beans and corn mixture. Mexican spices and seasonings. Topped with melted cheese. Served with fresh salsa."
            }
        ]
    }
    
    # Dinner Ideas - Mains 2
    mains2_json = {
        "filename": "Dinner Ideas - Mains_2.pdf",
        "sections": [
            {
                "page_number": 1,
                "heading": "Vegetable Curry",
                "text": "Mixed vegetables in aromatic curry sauce. Coconut milk and fresh spices. Basmati rice and naan bread. Fresh cilantro and lime garnish. Mild to spicy heat levels."
            },
            {
                "page_number": 1,
                "heading": "Falafel Platter",
                "text": "Crispy chickpea fritters. Fresh pita bread and hummus. Tahini sauce and pickled vegetables. Mixed green salad. Mediterranean flavors."
            },
            {
                "page_number": 1,
                "heading": "Pasta Primavera",
                "text": "Fresh seasonal vegetables. Al dente pasta of choice. Light cream sauce with herbs. Parmesan cheese garnish. Quick and delicious preparation."
            },
            {
                "page_number": 1,
                "heading": "Vegetable Stir Fry",
                "text": "Crisp vegetables in wok. Soy sauce and ginger marinade. Brown rice or quinoa base. Sesame seeds and green onions. Asian-inspired flavors."
            }
        ]
    }
    
    # Dinner Ideas - Mains 3
    mains3_json = {
        "filename": "Dinner Ideas - Mains_3.pdf",
        "sections": [
            {
                "page_number": 1,
                "heading": "Stuffed Portobello Mushrooms",
                "text": "Large portobello caps. Quinoa and vegetable stuffing. Balsamic glaze and herbs. Melted cheese topping. Elegant presentation."
            },
            {
                "page_number": 1,
                "heading": "Vegetable Paella",
                "text": "Saffron-infused rice dish. Mixed vegetables and legumes. Spanish paprika and herbs. Lemon wedges for garnish. Authentic Spanish flavors."
            },
            {
                "page_number": 1,
                "heading": "Lentil Shepherd's Pie",
                "text": "Mashed potato topping. Lentil and vegetable filling. Herbs and seasonings. Golden brown crust. Comfort food classic."
            },
            {
                "page_number": 1,
                "heading": "Vegetable Wellington",
                "text": "Puff pastry wrapped vegetables. Mushroom and spinach filling. Herb and garlic seasoning. Golden flaky crust. Elegant main course."
            }
        ]
    }
    
    # Dinner Ideas - Sides 1
    sides1_json = {
        "filename": "Dinner Ideas - Sides_1.pdf",
        "sections": [
            {
                "page_number": 1,
                "heading": "Roasted Vegetables",
                "text": "Assorted seasonal vegetables. Olive oil and herb seasoning. Caramelized edges and tender centers. Fresh herbs for garnish. Colorful and nutritious."
            },
            {
                "page_number": 1,
                "heading": "Quinoa Salad",
                "text": "Cooked quinoa with fresh vegetables. Lemon vinaigrette dressing. Fresh herbs and feta cheese. Light and refreshing side. Protein-rich option."
            },
            {
                "page_number": 1,
                "heading": "Garlic Mashed Potatoes",
                "text": "Creamy mashed potatoes. Roasted garlic and butter. Fresh herbs and seasoning. Smooth and comforting. Classic side dish."
            },
            {
                "page_number": 1,
                "heading": "Grilled Asparagus",
                "text": "Fresh asparagus spears. Olive oil and lemon seasoning. Parmesan cheese shavings. Tender and flavorful. Spring vegetable favorite."
            }
        ]
    }
    
    # Dinner Ideas - Sides 2
    sides2_json = {
        "filename": "Dinner Ideas - Sides_2.pdf",
        "sections": [
            {
                "page_number": 1,
                "heading": "Mediterranean Salad",
                "text": "Mixed greens and vegetables. Olive oil and balsamic dressing. Feta cheese and olives. Fresh herbs and spices. Light and refreshing."
            },
            {
                "page_number": 1,
                "heading": "Roasted Sweet Potatoes",
                "text": "Sweet potato wedges. Cinnamon and maple seasoning. Crispy edges and tender centers. Nutritious and delicious. Fall favorite."
            },
            {
                "page_number": 1,
                "heading": "Steamed Broccoli",
                "text": "Fresh broccoli florets. Light butter and lemon. Al dente texture. Simple and healthy. Classic green vegetable."
            },
            {
                "page_number": 1,
                "heading": "Couscous Pilaf",
                "text": "Fluffy couscous with vegetables. Herbs and spices. Light broth cooking. Flavorful and quick. Mediterranean side dish."
            }
        ]
    }
    
    # Dinner Ideas - Sides 3 (Gluten-Free)
    sides3_json = {
        "filename": "Dinner Ideas - Sides_3.pdf",
        "sections": [
            {
                "page_number": 1,
                "heading": "Cauliflower Rice",
                "text": "Riced cauliflower. Light seasoning and herbs. Low-carb alternative. Quick and healthy. Versatile side dish."
            },
            {
                "page_number": 1,
                "heading": "Zucchini Noodles",
                "text": "Spiralized zucchini. Light sauce and herbs. Low-carb pasta alternative. Fresh and crisp. Healthy noodle option."
            },
            {
                "page_number": 1,
                "heading": "Roasted Brussels Sprouts",
                "text": "Halved Brussels sprouts. Balsamic glaze and nuts. Caramelized edges. Nutritious and flavorful. Fall vegetable favorite."
            },
            {
                "page_number": 1,
                "heading": "Quinoa Pilaf",
                "text": "Cooked quinoa with vegetables. Herbs and light seasoning. Protein-rich side dish. Gluten-free grain option. Healthy and satisfying."
            }
        ]
    }
    
    # Dinner Ideas - Sides 4 (Buffet-Style)
    sides4_json = {
        "filename": "Dinner Ideas - Sides_4.pdf",
        "sections": [
            {
                "page_number": 1,
                "heading": "Mixed Green Salad",
                "text": "Fresh mixed greens. Assorted vegetables. Light vinaigrette. Croutons and nuts. Classic salad option."
            },
            {
                "page_number": 1,
                "heading": "Roasted Root Vegetables",
                "text": "Carrots, parsnips, and turnips. Herb and olive oil seasoning. Caramelized sweetness. Colorful presentation. Fall vegetable medley."
            },
            {
                "page_number": 1,
                "heading": "Wild Rice Blend",
                "text": "Mixed wild rice varieties. Vegetable broth cooking. Herbs and seasoning. Nutty and flavorful. Elegant side dish."
            },
            {
                "page_number": 1,
                "heading": "Steamed Green Beans",
                "text": "Fresh green beans. Light butter and herbs. Crisp-tender texture. Simple and healthy. Classic vegetable side."
            }
        ]
    }
    
    # Lunch Ideas
    lunch_json = {
        "filename": "Lunch Ideas.pdf",
        "sections": [
            {
                "page_number": 1,
                "heading": "Vegetarian Wraps",
                "text": "Fresh tortillas with vegetables. Hummus and avocado spread. Mixed greens and sprouts. Light and portable. Perfect for lunch."
            },
            {
                "page_number": 1,
                "heading": "Buddha Bowl",
                "text": "Quinoa or rice base. Assorted vegetables. Protein-rich legumes. Light dressing. Balanced meal option."
            },
            {
                "page_number": 1,
                "heading": "Mediterranean Platter",
                "text": "Hummus and pita bread. Fresh vegetables and olives. Feta cheese and nuts. Light and satisfying. Mediterranean flavors."
            },
            {
                "page_number": 1,
                "heading": "Vegetable Soup",
                "text": "Fresh seasonal vegetables. Light broth base. Herbs and seasoning. Warm and comforting. Healthy lunch option."
            }
        ]
    }
    
    # Save all JSON files
    all_jsons = [
        ("breakfast_ideas.json", breakfast_json),
        ("dinner_mains_1.json", mains1_json),
        ("dinner_mains_2.json", mains2_json),
        ("dinner_mains_3.json", mains3_json),
        ("dinner_sides_1.json", sides1_json),
        ("dinner_sides_2.json", sides2_json),
        ("dinner_sides_3.json", sides3_json),
        ("dinner_sides_4.json", sides4_json),
        ("lunch_ideas.json", lunch_json)
    ]
    
    for filename, content in all_jsons:
        json_file = json_dir / filename
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)
        print(f"Created: {filename}")

if __name__ == "__main__":
    create_menu_json_files()
    print("✅ All JSON files created successfully!") 