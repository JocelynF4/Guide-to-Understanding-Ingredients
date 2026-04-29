# Ingredient Assistant

A food label scanning tool for people who want to actually understand what they're eating. Built for anyone managing allergies, avoiding certain ingredients like preservatives, or just trying to make better choices at the grocery store. There is transparency about what is in your food, but that does not mean there is transparency about what it is doing there.

---

## The Problem

The idea came from something I've run into more than once. You're at the store, you pick up a product you are intrigued by, and you flip it over to check the ingredients. The list is there, and you recognize some of the basics like water and salt, but the rest might as well be written in a different language. You sort of vaguely recognize some of it, but you have no real idea what the purpose is, whether they're safe, or actively something you're trying to avoid. Ultimately you're putting your trust into CPG companies looking out for you and your health...that's not very realistic.

Now add an actual dietary restriction into that. If you have a nut allergy, a gluten sensitivity, or you're avoiding something specific for health reasons, reading food labels becomes genuinely stressful, and missing a couple words in small text could mean the difference between a deployed epipen. The "Contains:" statement helps, but it only covers the major allergens. If there is something not on there you want to avoid, be ready to spend the next few minutes until you give up squinting at the back of a product in the middle of the store.

That's the problem this tool is trying to solve. The Ingredient Assistant lets you point your camera at a food, beverage, or supplement product, and it tells you what's actually in it. It's plain English, describes what it is, what the purpose is, flagging anything that might be relevant to your health profile.

---

## System Diagram

Here is how the system works:

```mermaid
flowchart TD
    A[Scan product front] --> B[GPT-4o Vision: identify brand and product]
    B --> C[Search USDA FoodData Central]
    C --> D{Match found?}
    D -->|Confident match| E[Auto-select USDA record]
    D -->|Uncertain| F[User picks from candidates]
    D -->|No match| G[Scan ingredient panel directly]
    G --> H[GPT-4o reads label from image]
    E --> I[GPT-4o analyzes each ingredient]
    F --> I
    H --> I
    I --> J[Results surfaced: Green is Safe / Yellow is Health Flag/ Red is Allergen Detected]
    J --> K[User decides whether to buy]

    style A fill:#ADD8E6,stroke:#555
    style B fill:#ADD8E6,stroke:#555
    style C fill:#ADD8E6,stroke:#555
    style H fill:#ADD8E6,stroke:#555
    style I fill:#ADD8E6,stroke:#555
    style J fill:#ADD8E6,stroke:#555
    style K fill:#FFD700,stroke:#555
```

Blue nodes are AI steps. The yellow node is where the human takes over.

---

## AI Workflow

Here is what is actually happening with the AI:

```mermaid
flowchart LR
    A[Step 1: Scan product front] --> B[GPT-4o Vision]
    B --> C[Step 2: USDA API search]
    C --> D[Step 3: GPT-4o selects best match]
    D --> E[Step 4: Per-ingredient analysis]
    E --> F[Cross-check allergy profile]
    F --> G[Flagged output: Green / Yellow / Red]

    style A fill:#ADD8E6,stroke:#555
    style B fill:#ADD8E6,stroke:#555
    style C fill:#ADD8E6,stroke:#555
    style D fill:#ADD8E6,stroke:#555
    style E fill:#ADD8E6,stroke:#555
    style F fill:#ADD8E6,stroke:#555
    style G fill:#ADD8E6,stroke:#555
```

The allergy profile in the sidebar carries over the whole process. You can toggle the major allergens/avoidants and add your own custom ones (coconut, MSG, whatever applies to you).

The most important metric is accuracy for the AI, as having false positives could be life-threatening.

---

## Leverage Point

The leverage point is that this system utilizes to create the most impact is in closing the knowledge gap between a consumer's evaluation and purchase of a product while shopping. The gap is currently filled with trust, however misplaced, or with time-consuming scanning + googling words you don't know how to feel.

The Ingredient Assistant helps create impact by allowing the consumer to have control of that step, between evaluating alternatives and the purchase decision.

```mermaid
flowchart LR
    A[Food Label] --> B[Ingredient list: 75% unkown]
    B --> C{Ingredient Assistant}
    C --> D[Plain English explanations]
    C --> E[Purpose in this specific product]
    C --> F[Health flags]
    C --> G[Allergy alerts]
    D & E & F & G --> H[Informed purchase decision]

    style C fill:#FFD700,stroke:#555
    style H fill:#90EE90,stroke:#555
```

That middle is where this tool is. The ingredient list does not change, the only thing that does is whether someone can actually understand what they are looking at before they put it in their cart.

---

## Decision Boundary

The AI's only job is flagging the information. Everything after that is up to the user. The decision boundary is the step between knowledge, and action occuring from knowledge. If the emotional appeal of the product is strong, the knowledge about the ingredients won't matter. Another smaller decision boundary is when the solution asks if it has identified the product correctly, it's up to the user to confirm. The human in the loop is evident, as the process does not move forward without the user's permission and confirmation.

```mermaid
flowchart TD
    A[AI analysis complete: Green / Yellow / Red flags] --> B{Decision Boundary #1: Is this the right product?}
    B -->|No, override| C[Rescan or select different USDA match]
    C --> A
    B -->|Yes, confirmed| D[User reviews flagged ingredients]
    D --> E{Decision Boundary #2: Knowledge vs. Action}
    E --> F[Flag is relevant, I want to avoid this]
    E --> G[Flag noted, not a concern for me]
    E --> H[I really want this product anyway]
    F --> I[Put it back, find an alternative]
    G --> J[Buy it]
    H --> J

    style B fill:#FFD700,stroke:#555
    style E fill:#FFD700,stroke:#555
    style I fill:#90EE90,stroke:#555
    style J fill:#90EE90,stroke:#555
```

## Venture Description

This is a one-person tool meant for health-conscious and ingredient-avoiding consumers. The target user is anyone who reads food labels but struggles to actually understand them, people managing allergies, parents buying food for kids with sensitivities, and people trying to cut specific additives like artificial dyes.

The value proposition lies in the fact that you should not need a biochemistry degree or FDA job to know what you're consuming on a day-to-day. Place your trust in something factual and without agenda, which is not something most CPG companies can say.

The key activity and AI role is identification and recall. If this was an AI-team, the roles would primarily be in identifying the products, and retrieving the correlated information. Pretty simple task, but one where doing it without this tool would take significant time, and significant eye strain. People are curious, and care about the things that they consume, but see the cost and take the easy route. Ignorance is bliss. By using AI, consumers can get organized information quickly, and in plain English with one scan.

I believe the expected impact would be small, but a daily ritual. Most people have to go grocery shopping on a consistent basis, and often times feel the pressure of wanting to choose the healthy option, or be extra aware of allergens, but aren't willing to put in the time or effort. Offering that sense of security, of control is the real impact. People can know what they are consuming and why it's there.

---

## Responsible AI Reflection

The most serious risk is a false negative on an allergen. There can be a mixture of human and data error risks. Human error may be overlooking an alert (which would be hard because of the clear color coding) and the captured picture obscuring the ingredients. The data error risks would be that the USDA are inaccurate/unable to be pulled or that a product was recently reformulated and the database hasn't caught up. 

I have experimented around with some of the biases and seen them in action already. The USDA FoodData Central database includes many brands and products, however not all. Major national brands are included, but regional products, newer products, or even specifically Trader Joe's Chocolate Cups aren't recognized. I have not encountered a more robust database than the USDA one, but that data could come from partnerships with the FDA or with the manufacturers themselves. Another potential bias is the AI's view on whether something is truly a health flag or not. There may be many interpretations of what is not usual, and the role of the ingredient in the product requires context. Both items that are left up to the AI model's discretion introduce room for bias. 

There is definitely an over-reliance component in this venture, as it could be mistaken that the AI replaces reading the ingredient list. Because AI is confident about many things, it still requires some thought about if you want to consume the ingredient, health flag or not. Relying on the AI to tell you whether or not to consume something is not the purpose, it is more to give you the tools to understand. The decision to consume/purchase is still meant to lie with the now more informed user.

The limitations are that the system stops at flagging. It does not know the user's full medical history beyond the simple output, and it cannot get a deeper look into vague concepts like "natural flavors" because that information is not publicly disclosed. The AI is as limited as food labeling allows it to be. The Vision AI fallback for scanning ingredient panels directly is also genuinely less reliable than a structured database match, and users should treat those results with more skepticism.

The oversight that could occur is that this is an informational only tool, and does not suggest actions, or replace reading the label or talking to a clinician. A future improvement in terms of oversight would be to take into account the AI's overconfidence, and potentially show some kind of confidence indicator so users can tell when the AI is working from limited information. USDA records used in any analysis should show a last-updated date as well, so users can judge whether the formulation might have changed, and should be double checking the results of the Ingredient Assistant match the actual ingredients list. And for anyone flagging a severe or anaphylactic allergy in their profile, there should be an explicit reminder every single time that this tool is not sufficient on its own, and is not liable for consumer decisions.
