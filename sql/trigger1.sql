CREATE TRIGGER UpdateBusinessReviewStats
AFTER INSERT ON review
FOR EACH ROW
BEGIN
    -- Update review count
    UPDATE business
    SET review_count = (
        SELECT COUNT(*)
        FROM review
        WHERE review.business_id = NEW.business_id
    )
    WHERE business.business_id = NEW.business_id;

    -- Update average stars
    UPDATE business
    SET stars = (
        SELECT AVG(stars)
        FROM review
        WHERE review.business_id = NEW.business_id
    )
    WHERE business.business_id = NEW.business_id;

    -- Delete duplicate reviews, keeping only the most recent one
    DELETE FROM review
    WHERE review_id IN (
        SELECT review_id
        FROM review
        WHERE business_id = NEW.business_id
        AND user_id = NEW.user_id
        AND review_id NOT IN (
            SELECT review_id
            FROM review
            WHERE business_id = NEW.business_id
            AND user_id = NEW.user_id
            ORDER BY date DESC
            LIMIT 1
        )
    );
END;