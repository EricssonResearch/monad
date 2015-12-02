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
                //initialize notifications, temporary
                Storage.initializeNotificationData();
                Log.d(this.callingClassName, "Fake notifications have been generated");
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            Storage.initializeNotificationData();
            Log.d(this.callingClassName,
                    "Exception while loading notifications - Fake notifications have been generated");
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
