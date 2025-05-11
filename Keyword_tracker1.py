import json
from datetime import datetime

# Load post data
with open("dummy_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# Load keyword rules
with open("keywords.json", "r", encoding="utf-8") as f:
    keyword_rules = json.load(f)

# Keyword matching logic
def match_keywords(text, rule):
    txt = text.lower()
    if rule["logic"] == "AND":
        return all(kw.lower() in txt for kw in rule["keywords"])
    else:  # OR
        return any(kw.lower() in txt for kw in rule["keywords"])

# Process and simplify posts
simple_output = []
seen = set()

for post in posts:
    text = post.get("content", "")
    matched = []

    for rule in keyword_rules:
        if match_keywords(text, rule):
            matched.extend(rule["keywords"])

    if not matched:
        continue

    post_link = post.get("post_url")
    if post_link in seen:
        continue
    seen.add(post_link)

    simple_output.append({
        "post_link":        post_link,
        "user_profile_link": post.get("user_profile_url"),
        "username":         post.get("username"),
        "raw_post_content": post.get("content"),
        "num_likes":        post.get("likes", 0),
        "num_comments":     post.get("comments", 0),
        "date_posted":      post.get("date_posted"),
        "matched_keywords": list(set(matched)),
        "linkedin_profile_url": post.get("user_profile_url"),  # fallback, if scraping not done
        "date_extracted": datetime.utcnow().strftime("%Y-%m-%d")
    })

# Save to file
with open("all_matched_results.json", "w", encoding="utf-8") as f:
    json.dump(simple_output, f, indent=2)

print(f"Saved {len(simple_output)} simplified posts to all_matched_results.json")
