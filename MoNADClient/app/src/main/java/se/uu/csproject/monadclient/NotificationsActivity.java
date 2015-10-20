package se.uu.csproject.monadclient;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

import se.uu.csproject.monadclient.recyclerviews.NotificationRecyclerViewAdapter;
import se.uu.csproject.monadclient.recyclerviews.Notify;

//// TODO (low priority): receive data from notification module (maybe not in this activity - TBD), display them in notification bar as well as in the recyclerview
public class NotificationsActivity extends AppCompatActivity {

    public List<Notify> notifications;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_notifications);

        RecyclerView rv =(RecyclerView)findViewById(R.id.rv);

        LinearLayoutManager llm = new LinearLayoutManager(this);
        rv.setLayoutManager(llm);
        rv.setHasFixedSize(true);

        initializeData();
        NotificationRecyclerViewAdapter adapter = new NotificationRecyclerViewAdapter(notifications);
        rv.setAdapter(adapter);
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

}