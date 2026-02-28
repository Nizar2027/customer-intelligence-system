SELECT customer_id, category, COUNT(*) as cnt
FROM customer_interactions
GROUP BY customer_id, category
ORDER BY cnt DESC;




SELECT customer_id, MAX(transaction_date) AS last_visit
FROM transactions
GROUP BY customer_id;



SELECT customer_id, COUNT(*) AS total_transactions
FROM transactions
GROUP BY customer_id;
