import json
from datetime import datetime
import os

# Define the directory paths for your data files
keywords_dir = "keywords"  # Directory for keywords and ICP config files
results_dir = "results"    # Directory for saving the output

# 1. Load post data from the root directory
posts_file = "dummy_posts.json"  # File for posts data in the root directory
with open(posts_file, "r", encoding="utf-8") as f:
    posts = json.load(f)

# 2. Load keyword rules
keywords_file = os.path.join(keywords_dir, "keywords.json")  # File for keywords rules
with open(keywords_file, "r", encoding="utf-8") as f:
    keyword_rules = json.load(f)

# 3. Load ICP configuration
icp_config_file = os.path.join(keywords_dir, "icp_config.json")  # ICP config file
with open(icp_config_file, "r", encoding="utf-8") as f:
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
    combined = f"{profile_bio} {username}".lower() if profile_bio and username else ""
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
    score = min(round(score, 2), 1.0)
    return score

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

    # Calculate confidence
    confidence = calculate_confidence(post, matched_keywords, is_icp)

    # Generate reason for the match
    reason = generate_reason(post, is_icp, matched_keywords)

    # Append the post data to results
    results.append({
        "post_url": post_url,
        "poster_profile": post.get("user_profile_url"),
        "match_keyword": ", ".join(set(matched_keywords)),
        "confidence": confidence,
        "reason": reason,
        "date_extracted": datetime.utcnow().strftime("%Y-%m-%d")
    })

# 9. Save results
output_file = os.path.join(results_dir, "filtered_results.json")  # Output file for results
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

# 10. Print summary
print(f"Processed {len(results)} posts and saved to {output_file}")
