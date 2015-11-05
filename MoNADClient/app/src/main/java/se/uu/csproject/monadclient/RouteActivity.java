package se.uu.csproject.monadclient;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.Notify;
import se.uu.csproject.monadclient.recyclerviews.RouteRecyclerViewAdapter;

public class RouteActivity extends AppCompatActivity {

    RecyclerView recycler;
    boolean flagListVisible = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_route);
        Toolbar toolbar = (Toolbar)findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        recycler =(RecyclerView)findViewById(R.id.recycler);

        LinearLayoutManager llm = new LinearLayoutManager(this);
        recycler.setLayoutManager(llm);
        //recycler.setHasFixedSize(true);

        List<Notify> busStops = new ArrayList<>();
        initializeData(busStops);
        RouteRecyclerViewAdapter adapter = new RouteRecyclerViewAdapter(busStops);
        recycler.setAdapter(adapter);
        LinearLayout busStopListLayout = (LinearLayout) findViewById(R.id.layout_busstoplist);

        TextView timeStart = (TextView) findViewById(R.id.label_timestart);
        TextView walkStart = (TextView) findViewById(R.id.label_walkstart);
        TextView timeEnd = (TextView) findViewById(R.id.label_timeend);
        TextView walkEnd = (TextView) findViewById(R.id.label_walkend);

        Bundle b = getIntent().getExtras();
        final FullTrip trip = b.getParcelable("fulltrip");
        walkStart.setText("Walk to bus stop " + trip.getStartBusStop());
        timeStart.setText(formatTime(trip.getStartTime()));
        walkEnd.setText("Leave the bus at stop " + trip.getEndBusStop());
        timeEnd.setText(formatTime(trip.getEndTime()));

        Button btn_join_trips = (Button)findViewById(R.id.btn_join_trips);
        btn_join_trips.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                Intent myIntent = new Intent(RouteActivity.this, RouteConfirmPopup.class);
                myIntent.putExtra("selectedTrip", trip);
                RouteActivity.this.startActivity(myIntent);
            }
        });
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void expandBusStopList(View view){
        if(!flagListVisible){
            recycler.setVisibility(View.VISIBLE);
            flagListVisible = true;
        }
        else {
            recycler.setVisibility(View.GONE);
            flagListVisible = false;
        }
    }

    private String formatTime(Date date){
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
        return timeFormat.format(calendar.getTime());
    }

    private void initializeData(List<Notify> busStops){
        busStops.add(new Notify("Bus 805: 5 min delay", "15:59", R.drawable.ic_directions_bus_black_18dp));
        busStops.add(new Notify("Bus 805: Coming in 5 min", "15:43", R.drawable.ic_directions_bus_black_18dp));
        busStops.add(new Notify("Bus 805: Departing now", "15:38", R.drawable.ic_directions_bus_black_18dp));
        busStops.add(new Notify("Bus 801: 5 min delay", "15:15", R.drawable.ic_directions_bus_black_18dp));
        busStops.add(new Notify("Bus 801: Coming in 5 min", "15:11", R.drawable.ic_directions_bus_black_18dp));
        busStops.add(new Notify("Bus 801: Departing now", "15:06", R.drawable.ic_directions_bus_black_18dp));
        busStops.add(new Notify("Bus 805: 5 min delay", "15:59", R.drawable.ic_directions_bus_black_18dp));
        busStops.add(new Notify("Bus 805: Coming in 5 min", "15:43", R.drawable.ic_directions_bus_black_18dp));
        busStops.add(new Notify("Bus 805: Departing now", "15:38", R.drawable.ic_directions_bus_black_18dp));
        busStops.add(new Notify("Bus 801: 5 min delay", "15:15", R.drawable.ic_directions_bus_black_18dp));
        busStops.add(new Notify("Bus 801: Coming in 5 min", "15:11", R.drawable.ic_directions_bus_black_18dp));
        busStops.add(new Notify("Bus 801: Departing now", "15:06", R.drawable.ic_directions_bus_black_18dp));
    }
}
