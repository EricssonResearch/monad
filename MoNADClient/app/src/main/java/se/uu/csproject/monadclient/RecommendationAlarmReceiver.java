package se.uu.csproject.monadclient;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.support.v4.app.NotificationCompat;
import android.util.Log;

public class RecommendationAlarmReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent)
    {
        NotificationCompat.Builder mBuilder;
        mBuilder = new NotificationCompat.Builder(context);
        mBuilder.setSmallIcon(R.mipmap.ic_launcher);
        mBuilder.setContentTitle("Recommendation");
        mBuilder.setContentText("You have a new recommendation");
        mBuilder.setAutoCancel(true);
        mBuilder.setVibrate(new long[] { 1000, 1000, 1000 });

        NotificationManager mNotificationManager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);

        mNotificationManager.notify(NotificationsActivity.NOTIFICATION_ID, mBuilder.build());
    }
}
