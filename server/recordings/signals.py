def detection_post_save(sender, instance, created, **kwargs):
    if created:
        # Look for notifications.
        from recordings.models import (
            NotificationConfig,
            NOTIFICATION_TYPES,
            NOTIFICATION_DETECTION_TYPES,
        )
        from recordings.utils import send_notification_for_detection

        configs = NotificationConfig.objects.all().filter(
            notification_type=NOTIFICATION_TYPES.apprise, is_active=True
        )
        for config in configs:
            # Send on NOTIFICATION_DETECTION_TYPES.all
            if config.detection_type == NOTIFICATION_DETECTION_TYPES.all:
                send_notification_for_detection(instance, config)

            # Send on NOTIFICATION_DETECTION_TYPES.new_daily if is_unique_daily_detection
            instance.refresh_from_db()
            if (
                instance.is_unique_daily_detection
                and config.detection_type == NOTIFICATION_DETECTION_TYPES.new_daily
            ):
                send_notification_for_detection(instance, config)

            # Send on NOTIFICATION_DETECTION_TYPES.new_all_time if new_all_time
            if (
                instance.is_unique_alltime_detection
                and config.detection_type == NOTIFICATION_DETECTION_TYPES.new_all_time
            ):
                send_notification_for_detection(instance, config)
