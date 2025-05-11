import json
from datetime import datetime

# 1. Load post data
with open("dummy_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# 2. Load keyword rules
with open("keywords.json", "r", encoding="utf-8") as f:
    keyword_rules = json.load(f)

# 3. Load ICP configuration
with open("icp_config.json", "r", encoding="utf-8") as f:
    icp_config = json.load(f)
icp_keywords = icp_config.get("icp_keywords", [])

# 4. Keyword matching logic
def match_keywords(text, rule):
    txt = text.lower()
    if rule["logic"] == "AND":
        return all(kw.lower() in txt for kw in rule["keywords"])
    else:  # OR
        return any(kw.lower() in txt for kw in rule["keywords"])

# 5. ICP matching logic
def matches_icp(profile_bio, username):
    combined = f"{profile_bio} {username}".lower()
    return any(kw.lower() in combined for kw in icp_keywords)

# 6. Confidence scoring logic
def calculate_confidence(post, matched_keywords, is_icp):
    score = 0.0
    score += len(set(matched_keywords)) * 0.2
    if is_icp:
        score += 0.3
    if post.get("likes", 0) > 10:
        score += 0.1
    if post.get("comments", 0) > 3:
        score += 0.1
    return min(round(score, 2), 1.0)

# 7. Generate reason
def generate_reason(post, is_icp, matched_keywords):
    parts = []
    if matched_keywords:
        parts.append("Matched keyword(s): " + ", ".join(set(matched_keywords)))
    if is_icp:
        parts.append("Bio matches ICP criteria")
    if post.get("likes", 0) > 10 or post.get("comments", 0) > 3:
        parts.append("Post shows engagement")
    return "; ".join(parts)

# 8. Process posts
results = []
seen_urls = set()

for post in posts:
    text = post.get("content", "")
    matched_keywords = []

    # Match keywords
    for rule in keyword_rules:
        if match_keywords(text, rule):
            matched_keywords.extend(rule["keywords"])

    if not matched_keywords:
        continue  # No keyword match, skip

    # Match ICP
    is_icp = matches_icp(post.get("bio", ""), post.get("username", ""))
    if not is_icp:
        continue  # No ICP match, skip

    post_url = post.get("post_url")
    if post_url in seen_urls:
        continue
    seen_urls.add(post_url)

    confidence = calculate_confidence(post, matched_keywords, is_icp)
    reason = generate_reason(post, is_icp, matched_keywords)

    results.append({
        "post_url": post_url,
        "poster_profile": post.get("user_profile_url"),
        "match_keyword": ", ".join(set(matched_keywords)),
        "confidence": confidence,
        "reason": reason,
        "date_extracted": datetime.utcnow().strftime("%Y-%m-%d")
    })

# 9. Save results
with open("filtered_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Saved {len(results)} leads to filtered_results.json")
