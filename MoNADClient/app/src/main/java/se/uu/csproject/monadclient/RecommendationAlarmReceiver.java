package se.uu.csproject.monadclient;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.support.v4.app.NotificationCompat;

import se.uu.csproject.monadclient.activities.NotificationsActivity;
import se.uu.csproject.monadclient.activities.RouteActivity;
import se.uu.csproject.monadclient.serverinteractions.ClientAuthentication;

public class RecommendationAlarmReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        //if the user logged out, or the application is killed, the notification will not appear
        if (ClientAuthentication.getClientId() == null || ClientAuthentication.getClientId().equals("")){
            return;
        }

        Intent newintent = new Intent(context.getApplicationContext(), RouteActivity.class);
        newintent.putExtra("selectedTrip", intent.getParcelableExtra("selectedTrip"));

        newintent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent pendingIntent = PendingIntent.getActivity(context.getApplicationContext(), 0, newintent,
                PendingIntent.FLAG_UPDATE_CURRENT);

        NotificationCompat.Builder mBuilder;
        mBuilder = new NotificationCompat.Builder(context);
        mBuilder.setSmallIcon(R.mipmap.ic_launcher);
        mBuilder.setContentTitle("Recommendation");
        mBuilder.setContentText("You have a new recommendation");
        mBuilder.setAutoCancel(true);
        mBuilder.setVibrate(new long[]{1000, 1000, 1000});
        mBuilder.setContentIntent(pendingIntent);

        NotificationManager mNotificationManager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);

        mNotificationManager.notify(NotificationsActivity.NOTIFICATION_ID, mBuilder.build());
    }
}
