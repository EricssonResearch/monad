package se.uu.csproject.monadclient;

import android.app.NotificationManager;
import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.NavUtils;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;

import java.util.ArrayList;
import java.util.List;

import se.uu.csproject.monadclient.recyclerviews.NotificationRecyclerViewAdapter;
import se.uu.csproject.monadclient.recyclerviews.Notify;

//// TODO (low priority): receive data from notification module (maybe not in this activity - TBD), display them in notification bar as well as in the recyclerview
public class NotificationsActivity extends AppCompatActivity {

    public static List<Notify> notifications;
    public static int NOTIFICATION_ID = 100;
    public static String NOTIFICATION_ID_STR = "_id";
    View view;
    ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_notifications);

        RecyclerView rv =(RecyclerView)findViewById(R.id.rv);

        LinearLayoutManager llm = new LinearLayoutManager(this);
        rv.setLayoutManager(llm);
        rv.setHasFixedSize(true);

        initializeData();
        NotificationRecyclerViewAdapter adapter;
        adapter = new NotificationRecyclerViewAdapter(getApplicationContext(), notifications);
        rv.setAdapter(adapter);


        NotificationManager mNotificationManager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        mNotificationManager.cancel(getIntent().getIntExtra(NOTIFICATION_ID_STR, -1));






    }


    private void initializeData(){
                notifications = new ArrayList<>();
                notifications.add(new Notify("Bus 805: 5 min delay", "15:59", R.drawable.ic_assistant_photo_black_24dp));
                notifications.add(new Notify("Bus 805: Coming in 5 min", "15:43", R.drawable.ic_feedback_black_24dp));
                notifications.add(new Notify("Bus 805: Departing now", "15:38", R.drawable.ic_alarm_black_24dp));
                notifications.add(new Notify("Bus 801: 5 min delay", "15:15", R.drawable.ic_assistant_photo_black_24dp));
                notifications.add(new Notify("Bus 801: Coming in 5 min", "15:11", R.drawable.ic_feedback_black_24dp));
                notifications.add(new Notify("Bus 801: Departing now", "15:06", R.drawable.ic_alarm_black_24dp));
            }
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        if(id == android.R.id.home){
            NavUtils.navigateUpFromSameTask(this);
        }

        if (id == R.id.action_search) {
            return true;
        }

        if (id == R.id.action_notifications) {
            startActivity(new Intent(this, NotificationsActivity.class));
        }

        if (id == R.id.action_mytrips) {
            startActivity(new Intent(this, TripsActivity.class));
        }

        if (id == R.id.action_profile) {
            startActivity(new Intent(this, ProfileActivity.class));
        }

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            startActivity(new Intent(this, SettingsActivity.class));
        }

        if (id == R.id.action_aboutus) {
            //TODO (low priority): Create a toaster with text about the MoNAD project and team
            startActivity(new Intent(this, AboutUsActivity.class));
        }

        if (id == R.id.action_signout) {
            startActivity(new Intent(this, LoginActivity.class));
        }

        return super.onOptionsItemSelected(item);
    }


}





