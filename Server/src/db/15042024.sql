ALTER TABLE `canvas_clone`.`User`
ADD COLUMN `first_name` VARCHAR(255) NOT NULL AFTER `role`,
ADD COLUMN `last_name` VARCHAR(255) NOT NULL AFTER `first_name`,
ADD COLUMN `notification` TINYINT NOT NULL AFTER `last_name`;
