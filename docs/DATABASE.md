Volume 3: Database Design
The central object is the Intelligence Item.
Core Tables
topics
sources
intelligence_items
tags
item_tags
entities
item_entities
story_clusters
daily_briefs
ingestion_runs
Key Relationships
One source has many intelligence items.
One topic has many intelligence items.
One intelligence item may have many tags.
One intelligence item may belong to one story cluster.
One story cluster may contain many intelligence items.
One daily brief summarizes many intelligence items.
Intelligence Item Fields
id
source_id
topic_id
cluster_id
title
url
canonical_url
item_type
published_at
discovered_at
raw_content
cleaned_content
summary
ai_significance
language
authority_score
relevance_score
embedding
created_at
updated_at
