# ml/recommendations.py — Smart Diet & Exercise Recommendations
# Based on: arthritis type + pain level + symptoms + biomarkers

ARTHRITIS_DIET = {
    'Rheumatoid Arthritis (RA)': {
        'focus': 'Anti-inflammatory omega-3 rich diet to reduce joint inflammation and autoimmune activity.',
        'best_foods': [
            {'name': 'Fatty Fish (Salmon, Sardines)', 'reason': 'High in Omega-3 fatty acids which reduce inflammatory cytokines', 'emoji': '🐟'},
            {'name': 'Turmeric & Ginger',             'reason': 'Curcumin in turmeric blocks NF-kB, a key inflammation trigger', 'emoji': '🌿'},
            {'name': 'Leafy Greens (Spinach, Kale)',  'reason': 'Rich in Vitamin K and antioxidants that protect joint tissue', 'emoji': '🥬'},
            {'name': 'Berries (Blueberry, Strawberry)','reason': 'Anthocyanins reduce oxidative stress in inflamed joints',     'emoji': '🫐'},
            {'name': 'Olive Oil (Extra Virgin)',       'reason': 'Oleocanthal acts like ibuprofen — natural anti-inflammatory',  'emoji': '🫒'},
            {'name': 'Walnuts & Flaxseeds',            'reason': 'Plant-based Omega-3 (ALA) reduces morning stiffness',          'emoji': '🌰'},
            {'name': 'Green Tea',                      'reason': 'EGCG antioxidant reduces cartilage breakdown in RA',           'emoji': '🍵'},
        ],
        'avoid': [
            {'name': 'Red Meat',         'reason': 'High arachidonic acid worsens inflammation'},
            {'name': 'Processed Foods',  'reason': 'Trans fats and additives spike inflammatory markers'},
            {'name': 'Sugar & Soda',     'reason': 'Raises CRP levels — your inflammation marker'},
            {'name': 'Gluten (if sensitive)', 'reason': 'Can trigger autoimmune flares in RA patients'},
            {'name': 'Alcohol',          'reason': 'Interacts with RA medications, worsens inflammation'},
        ],
        'meal_plan': {
            'Breakfast': 'Oatmeal with walnuts, blueberries and flaxseeds + green tea',
            'Lunch':     'Grilled salmon with spinach salad, olive oil dressing + turmeric rice',
            'Dinner':    'Lentil soup with leafy greens + ginger-turmeric herbal tea',
            'Snack':     'Handful of walnuts + a bowl of mixed berries'
        }
    },
    'Osteoarthritis (OA)': {
        'focus': 'Joint-protective diet rich in collagen builders, Vitamin D, and calcium to slow cartilage breakdown.',
        'best_foods': [
            {'name': 'Bone Broth',                    'reason': 'Natural collagen and glucosamine to rebuild cartilage',         'emoji': '🍲'},
            {'name': 'Dairy (Low-fat milk, Yogurt)',   'reason': 'Calcium + Vitamin D critical for bone density in OA',          'emoji': '🥛'},
            {'name': 'Eggs',                          'reason': 'Vitamin D and protein for muscle support around joints',        'emoji': '🥚'},
            {'name': 'Citrus Fruits (Orange, Lemon)',  'reason': 'Vitamin C stimulates collagen synthesis for cartilage repair',  'emoji': '🍊'},
            {'name': 'Broccoli & Cauliflower',         'reason': 'Sulforaphane blocks enzymes that destroy cartilage',           'emoji': '🥦'},
            {'name': 'Avocado',                        'reason': 'ASU compounds in avocado slow OA progression clinically',      'emoji': '🥑'},
            {'name': 'Pineapple',                      'reason': 'Bromelain enzyme reduces joint swelling and stiffness',        'emoji': '🍍'},
        ],
        'avoid': [
            {'name': 'Fried Foods',      'reason': 'Advanced glycation end products (AGEs) damage cartilage'},
            {'name': 'White Bread/Rice', 'reason': 'High glycemic index increases inflammation in joints'},
            {'name': 'Excess Salt',      'reason': 'Worsens water retention causing joint pressure'},
            {'name': 'Omega-6 rich oils','reason': 'Corn/sunflower oil tips Omega-3:6 ratio toward inflammation'},
        ],
        'meal_plan': {
            'Breakfast': 'Scrambled eggs with broccoli + orange juice + low-fat yogurt',
            'Lunch':     'Bone broth soup with vegetables + avocado salad',
            'Dinner':    'Grilled chicken with cauliflower + pineapple slices',
            'Snack':     'Low-fat milk + a citrus fruit'
        }
    },
    'Gout': {
        'focus': 'Low-purine diet to reduce uric acid buildup — the direct cause of gout attacks.',
        'best_foods': [
            {'name': 'Cherries (Fresh or Juice)',      'reason': 'Anthocyanins directly lower uric acid levels — proven in trials','emoji': '🍒'},
            {'name': 'Low-fat Dairy',                  'reason': 'Casein and lactalbumin proteins promote uric acid excretion',   'emoji': '🥛'},
            {'name': 'Coffee (Black)',                 'reason': 'Studies show 2 cups/day reduces gout attack risk by 40%',       'emoji': '☕'},
            {'name': 'Water (3+ litres/day)',          'reason': 'Flushes uric acid through kidneys — most important for gout',   'emoji': '💧'},
            {'name': 'Vegetables (all types)',         'reason': 'Despite purines, vegetable purines do NOT raise uric acid',     'emoji': '🥗'},
            {'name': 'Whole Grains',                   'reason': 'Complex carbs lower insulin resistance linked to gout',         'emoji': '🌾'},
        ],
        'avoid': [
            {'name': 'Red Meat & Organ Meat', 'reason': 'Extremely high purines — directly raises uric acid to attack levels'},
            {'name': 'Shellfish & Anchovies', 'reason': 'Among highest purine foods — triggers acute gout attacks'},
            {'name': 'Beer & Alcohol',        'reason': 'Alcohol blocks uric acid excretion AND beer has purines'},
            {'name': 'Sugary Drinks (Fructose)','reason': 'Fructose metabolism produces uric acid as a byproduct'},
            {'name': 'Asparagus, Mushrooms',  'reason': 'Moderately high purines — limit during flares'},
        ],
        'meal_plan': {
            'Breakfast': 'Oatmeal with skimmed milk + cherry juice (100ml) + black coffee',
            'Lunch':     'Vegetable soup with whole grain bread + low-fat yogurt',
            'Dinner':    'Steamed vegetables with tofu + brown rice + water',
            'Snack':     'Fresh cherries or cherry extract + plenty of water'
        }
    },
    'Psoriatic Arthritis': {
        'focus': 'Anti-inflammatory diet targeting both skin and joint symptoms, with gut health focus.',
        'best_foods': [
            {'name': 'Fatty Fish',                    'reason': 'Omega-3 reduces both skin plaques and joint inflammation',      'emoji': '🐟'},
            {'name': 'Probiotic Foods (Yogurt, Kefir)','reason': 'Gut microbiome balance linked to psoriatic flare reduction',  'emoji': '🥛'},
            {'name': 'Colorful Vegetables',           'reason': 'Beta-carotene and lycopene reduce skin inflammation',           'emoji': '🫑'},
            {'name': 'Turmeric',                      'reason': 'Curcumin reduces both IL-17 (skin) and TNF-α (joint) markers', 'emoji': '🌿'},
            {'name': 'Zinc-rich Foods (Pumpkin seeds)','reason': 'Zinc deficiency worsens psoriatic skin and joint symptoms',   'emoji': '🎃'},
        ],
        'avoid': [
            {'name': 'Nightshades (Tomato, Pepper)', 'reason': 'Can trigger flares in some psoriatic arthritis patients'},
            {'name': 'Gluten',                        'reason': 'Strong link between celiac-like sensitivity and psoriatic flares'},
            {'name': 'Alcohol',                       'reason': 'Directly worsens psoriasis and interacts with methotrexate'},
            {'name': 'Processed Sugar',               'reason': 'Feeds inflammatory pathways via AGE production'},
        ],
        'meal_plan': {
            'Breakfast': 'Kefir smoothie with berries and turmeric + pumpkin seeds',
            'Lunch':     'Grilled salmon with colorful roasted vegetables + brown rice',
            'Dinner':    'Chicken curry with turmeric and coconut milk + quinoa',
            'Snack':     'Probiotic yogurt + mixed seeds'
        }
    },
    'Ankylosing Spondylitis': {
        'focus': 'Anti-inflammatory diet with focus on gut health (strong gut-spine axis link) and bone density.',
        'best_foods': [
            {'name': 'Probiotic Foods',               'reason': 'AS has strong gut microbiome connection — Klebsiella link',     'emoji': '🥛'},
            {'name': 'Calcium-rich Foods',            'reason': 'Spinal fusion risk makes bone density critical',                'emoji': '🧀'},
            {'name': 'Vitamin D Foods + Sunlight',    'reason': 'Deficiency worsens AS progression and bone loss',               'emoji': '☀️'},
            {'name': 'Anti-inflammatory Herbs',       'reason': 'Boswellia and turmeric shown to reduce AS inflammation',        'emoji': '🌿'},
            {'name': 'Lean Protein',                  'reason': 'Supports muscle strength around the spine',                     'emoji': '🍗'},
        ],
        'avoid': [
            {'name': 'High-starch Foods',  'reason': 'Klebsiella bacteria (linked to AS) feeds on starch'},
            {'name': 'Excess Red Meat',    'reason': 'Arachidonic acid worsens spinal inflammation'},
            {'name': 'Alcohol',            'reason': 'Reduces bone density and worsens gut permeability'},
        ],
        'meal_plan': {
            'Breakfast': 'Probiotic yogurt with seeds + calcium-fortified milk + sunlight walk',
            'Lunch':     'Grilled chicken with leafy greens + calcium-rich cheese + turmeric tea',
            'Dinner':    'Fish curry with low-starch vegetables + small portion brown rice',
            'Snack':     'Kefir drink + vitamin D supplement with meal'
        }
    },
    'Juvenile Idiopathic Arthritis': {
        'focus': 'Nutrient-dense anti-inflammatory diet supporting growth while managing inflammation.',
        'best_foods': [
            {'name': 'Calcium & Vitamin D Foods',     'reason': 'Critical for bone growth — JIA increases fracture risk',        'emoji': '🥛'},
            {'name': 'Omega-3 Rich Foods',            'reason': 'Reduces inflammation without side effects in children',         'emoji': '🐟'},
            {'name': 'Colorful Fruits & Vegetables',  'reason': 'Antioxidants protect growing joints from oxidative damage',     'emoji': '🍎'},
            {'name': 'Lean Protein',                  'reason': 'Supports muscle development around affected joints',            'emoji': '🍗'},
            {'name': 'Iron-rich Foods',               'reason': 'JIA causes anemia — iron-rich foods help correct this',         'emoji': '🥩'},
        ],
        'avoid': [
            {'name': 'Sugary Snacks & Drinks', 'reason': 'Increases inflammation and affects medication effectiveness'},
            {'name': 'Processed/Fast Food',    'reason': 'Trans fats worsen joint inflammation in children'},
            {'name': 'Excess Caffeine',        'reason': 'Interferes with calcium absorption critical for growing bones'},
        ],
        'meal_plan': {
            'Breakfast': 'Fortified milk + eggs + fruit smoothie with flaxseeds',
            'Lunch':     'Tuna sandwich on whole grain + vegetable sticks + milk',
            'Dinner':    'Grilled fish with broccoli + sweet potato + yogurt',
            'Snack':     'Fruit + handful of nuts + calcium-rich cheese'
        }
    }
}

PAIN_EXERCISE = {
    'low': {  # pain 0-3
        'label': 'Low Pain — Active Recovery',
        'description': 'Your pain is well controlled. You can do moderate exercise to strengthen muscles and improve joint mobility.',
        'exercises': [
            {'name': 'Brisk Walking',         'duration': '30-45 min', 'type': 'cardio',     'benefit': 'Improves circulation and reduces joint stiffness', 'emoji': '🚶'},
            {'name': 'Swimming / Water Aerobics','duration': '30 min',  'type': 'cardio',     'benefit': 'Zero-impact full-body movement, ideal for all joints','emoji': '🏊'},
            {'name': 'Cycling (Stationary)',  'duration': '20-30 min', 'type': 'cardio',     'benefit': 'Strengthens quadriceps which support knee joints',  'emoji': '🚴'},
            {'name': 'Yoga (Hatha/Restorative)','duration': '30 min',  'type': 'flexibility','benefit': 'Improves range of motion and reduces morning stiffness','emoji': '🧘'},
            {'name': 'Resistance Band Exercises','duration': '20 min', 'type': 'strength',   'benefit': 'Builds muscle around joints without heavy load',     'emoji': '💪'},
            {'name': 'Tai Chi',               'duration': '20-30 min', 'type': 'balance',    'benefit': 'Improves balance, reduces fall risk and joint stress','emoji': '🥋'},
        ],
        'daily_steps': '6,000 – 8,000 steps',
        'rest_advice': 'Take 5-min breaks every hour if sitting. Stretch every morning.'
    },
    'moderate': {  # pain 4-6
        'label': 'Moderate Pain — Gentle Movement',
        'description': 'Move gently to prevent stiffness but avoid high-impact activities. Rest is important but complete inactivity worsens stiffness.',
        'exercises': [
            {'name': 'Gentle Walking',        'duration': '15-20 min', 'type': 'cardio',     'benefit': 'Maintains mobility without overloading joints',      'emoji': '🚶'},
            {'name': 'Chair Yoga',            'duration': '15-20 min', 'type': 'flexibility','benefit': 'Seated stretching reduces stiffness safely',          'emoji': '🪑'},
            {'name': 'Warm Water Therapy',    'duration': '20 min',    'type': 'therapy',    'benefit': 'Warm water relaxes muscles and reduces pain signals',  'emoji': '🛁'},
            {'name': 'Gentle Stretching',     'duration': '10-15 min', 'type': 'flexibility','benefit': 'Reduces morning stiffness and improves blood flow',    'emoji': '🤸'},
            {'name': 'Deep Breathing',        'duration': '10 min',    'type': 'relaxation', 'benefit': 'Reduces inflammation response via vagal nerve',       'emoji': '🫁'},
        ],
        'daily_steps': '3,000 – 5,000 steps',
        'rest_advice': 'Apply warm compress before exercise. Ice joints after if swollen.'
    },
    'high': {  # pain 7-10
        'label': 'High Pain — Rest & Recovery',
        'description': 'Pain is high — prioritize rest and gentle therapeutic movement only. Do not push through severe pain.',
        'exercises': [
            {'name': 'Gentle Range of Motion', 'duration': '5-10 min','type': 'therapy',    'benefit': 'Prevents joint stiffness during flare without stress', 'emoji': '🤲'},
            {'name': 'Deep Breathing / Meditation','duration': '15 min','type': 'relaxation','benefit': 'Activates parasympathetic system, reduces pain perception','emoji': '🧘'},
            {'name': 'Seated Ankle/Wrist Circles','duration': '5 min', 'type': 'flexibility','benefit': 'Maintains circulation in affected joints during rest',  'emoji': '🦶'},
            {'name': 'Cold/Heat Therapy',      'duration': '15-20 min','type': 'therapy',   'benefit': 'Ice reduces acute swelling; heat relaxes stiff muscles', 'emoji': '🧊'},
        ],
        'daily_steps': '1,000 – 2,000 steps (or as tolerated)',
        'rest_advice': 'Rest in a comfortable position. Elevate swollen joints. Contact doctor if pain > 8 for 3+ days.'
    }
}

SYMPTOM_EXPLANATIONS = {
    'crp': {
        'name': 'C-Reactive Protein (CRP)',
        'normal': '< 10 mg/L',
        'what_is': 'A protein made by your liver in response to inflammation anywhere in the body.',
        'high_means': 'Active inflammation in your joints. High CRP (>10) suggests your arthritis is currently flaring.',
        'icon': '🔬'
    },
    'esr': {
        'name': 'Erythrocyte Sedimentation Rate (ESR)',
        'normal': 'Men < 15 mm/hr, Women < 20 mm/hr',
        'what_is': 'Measures how fast red blood cells settle — faster settling = more inflammation proteins in blood.',
        'high_means': 'Systemic inflammation. High ESR is a key marker for RA and other inflammatory arthritis types.',
        'icon': '🩸'
    },
    'rf_factor': {
        'name': 'Rheumatoid Factor (RF)',
        'normal': '< 14 IU/mL',
        'what_is': 'An antibody that attacks your own body — its presence suggests an autoimmune process.',
        'high_means': 'Strong indicator of Rheumatoid Arthritis. 70-80% of RA patients have elevated RF.',
        'icon': '🧬'
    },
    'uric_acid': {
        'name': 'Uric Acid',
        'normal': 'Men < 7.0 mg/dL, Women < 6.0 mg/dL',
        'what_is': 'A waste product from breaking down purines found in certain foods and your own cells.',
        'high_means': 'Uric acid crystals form in joints causing extreme pain — this is exactly what causes Gout attacks.',
        'icon': '💎'
    },
    'morning_stiffness': {
        'name': 'Morning Stiffness',
        'normal': '< 30 minutes',
        'what_is': 'Joint stiffness that occurs after waking or inactivity, caused by fluid buildup and inflammation.',
        'high_means': 'Stiffness > 1 hour is a hallmark of Rheumatoid Arthritis. OA stiffness usually resolves within 30 mins.',
        'icon': '🌅'
    },
    'swelling': {
        'name': 'Joint Swelling',
        'normal': 'No visible swelling',
        'what_is': 'Excess fluid (synovial fluid) in the joint space caused by the immune system attacking the joint lining.',
        'high_means': 'Active synovitis (inflamed joint lining). Indicates disease activity — may need medication adjustment.',
        'icon': '💧'
    },
    'anti_ccp': {
        'name': 'Anti-CCP Antibody',
        'normal': '< 20 U/mL',
        'what_is': 'A very specific antibody to Cyclic Citrullinated Peptides — almost exclusively found in RA.',
        'high_means': 'Highly specific for Rheumatoid Arthritis (95% specificity). Can appear years BEFORE symptoms.',
        'icon': '🧬'
    },
    'fatigue': {
        'name': 'Fatigue in Arthritis',
        'normal': 'Fatigue level 0-3',
        'what_is': 'Extreme tiredness beyond normal tiredness — caused by inflammatory cytokines affecting the brain and body.',
        'high_means': 'High fatigue (>6) indicates active inflammation systemically. Common in RA, AS, and Psoriatic Arthritis.',
        'icon': '😴'
    }
}

def get_pain_level(pain_score):
    if pain_score <= 3:   return 'low'
    elif pain_score <= 6: return 'moderate'
    else:                 return 'high'

def get_recommendations(arthritis_type, pain_score, symptoms=None):
    pain_level = get_pain_level(pain_score)
    diet = ARTHRITIS_DIET.get(arthritis_type, ARTHRITIS_DIET['Osteoarthritis (OA)'])
    exercise = PAIN_EXERCISE[pain_level]

    # Symptom explanations for any flagged symptoms
    explanations = {}
    if symptoms:
        for key in symptoms:
            if key in SYMPTOM_EXPLANATIONS:
                explanations[key] = SYMPTOM_EXPLANATIONS[key]

    return {
        'diet':         diet,
        'exercise':     exercise,
        'pain_level':   pain_level,
        'explanations': explanations
    }
