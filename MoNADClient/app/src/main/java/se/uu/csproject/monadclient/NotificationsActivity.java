package se.uu.csproject.monadclient;

import android.app.NotificationManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;

import java.util.ArrayList;

import se.uu.csproject.monadclient.interfaces.AsyncNotificationsInteraction;
import se.uu.csproject.monadclient.recyclerviews.NotificationRecyclerViewAdapter;
import se.uu.csproject.monadclient.recyclerviews.Notify;
import se.uu.csproject.monadclient.recyclerviews.Storage;

//// TODO (low priority): receive data from notification module (maybe not in this activity - TBD), display them in notification bar as well as in the recyclerview
//public class NotificationsActivity extends MenuedActivity implements AsyncResponse, AsyncNotificationsInteraction {
public class NotificationsActivity extends MenuedActivity implements AsyncNotificationsInteraction {
    private Toolbar toolbar;
    public static ArrayList<Notify> notifications;
//    private ArrayList<FullTrip> bookings;
    public static int NOTIFICATION_ID = 100;
    public static String NOTIFICATION_ID_STR = "_id";
    View view;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_notifications);

        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setHomeAsUpIndicator(R.drawable.ic_home_white_24dp);

        NotificationManager mNotificationManager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        mNotificationManager.cancel(getIntent().getIntExtra(NOTIFICATION_ID_STR, -1));
    }

    // Gets the user's bookings from the server
//    private void getBookings(){
//        String userId = ClientAuthentication.getClientId();
//        SendUserBookingsRequest asyncTask = new SendUserBookingsRequest();
//        asyncTask.delegate = this;
//        asyncTask.execute(userId);
//    }

    // Deals with the response by the server
//    public void processFinish(ArrayList<FullTrip> bookings){
//        if (!bookings.isEmpty()){
//            this.bookings = bookings;
//            Storage.setBookings(bookings);
//        }
//        displayNotifications();
//    }

    public boolean onCreateOptionsMenu(Menu menu) {

        if (ClientAuthentication.getPassword().equals("0")) {
            // Inflate the menu; this adds items to the action bar if it is present.
            getMenuInflater().inflate(R.menu.menu_main_google, menu);
            return true;
        }
        else {
            getMenuInflater().inflate(R.menu.menu_main, menu);
            return true;
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        getNotifications();
//        bookings = Storage.getBookings();
//        if (bookings.isEmpty()){
//            getBookings();
//        } else {
//            displayNotifications();
//        }
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == R.id.action_notifications) {
            getNotifications();
            return true;
        }
        else {
            return super.onOptionsItemSelected(item);
        }
    }

    public void getNotifications() {
        Storage.clearNotifications();
        new GetNotificationsTask(this).executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
    }

    @Override
    public void processReceivedNotifications() {
        displayNotifications();
    }

    public void displayNotifications() {
        RecyclerView rv = (RecyclerView) findViewById(R.id.rv);

        LinearLayoutManager llm = new LinearLayoutManager(this);
        rv.setLayoutManager(llm);
        rv.setHasFixedSize(true);

        notifications = Storage.getNotifications();

        NotificationRecyclerViewAdapter adapter;
//        adapter = new NotificationRecyclerViewAdapter(getApplicationContext(), notifications, bookings);
        adapter = new NotificationRecyclerViewAdapter(getApplicationContext(), notifications);
        rv.setAdapter(adapter);
    }
}