package se.uu.csproject.monadclient;

import android.os.AsyncTask;
import android.util.Log;

import se.uu.csproject.monadclient.storage.Storage;

/**
 *
 */
public class NotificationsInteraction {
    private String callingClassName;

    private class GetNotificationsTask extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... params) {
            String response = ClientAuthentication.postGetNotificationsRequest();
            return response;
        }
    }

    private class RemoveNotificationTask extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... params) {
            String response = ClientAuthentication.postRemoveNotificationRequest(params[0]);
            return response;
        }
    }

    public NotificationsInteraction(String callingClassName) {
        this.callingClassName = callingClassName;
    }

    public void getNotifications() {
        Storage.clearNotifications();
        GetNotificationsTask notificationsTask = new GetNotificationsTask();
        try {
            String response = notificationsTask.execute().get();
            System.out.println("Response: " + response);

            if (response.equals("1")) {
                Log.d(this.callingClassName, "Notifications have been successfully loaded by the database");
            }
            else {
                Log.d(this.callingClassName, "Could not load notifications");
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            Log.d(this.callingClassName,
                    "Exception while loading notifications - Could not load notifications");
        }
    }

    public void removeNotification(int i) {
        RemoveNotificationTask task = new RemoveNotificationTask();
        try {
            String response = task.execute(Storage.getNotifications().get(i).getID()).get();

            if (response.equals("1")) {
                Log.d(this.callingClassName, "Notification was successfully removed from the database");
            }
            else {
                Log.d(this.callingClassName, "Notification was not removed from the database");
            }
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }
}
