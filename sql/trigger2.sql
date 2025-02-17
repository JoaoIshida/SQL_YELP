CREATE TRIGGER EnforceTipReviewConstraint
BEFORE INSERT ON tip
FOR EACH ROW
BEGIN
    -- Check if the user has reviewed the business
    SELECT CASE
        WHEN NOT EXISTS (
            SELECT 1
            FROM review
            WHERE review.user_id = NEW.user_id
            AND review.business_id = NEW.business_id
        ) THEN
            RAISE(ABORT, 'Users can only give tips for businesses they have previously reviewed.')
    END;
END;