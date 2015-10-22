package se.uu.csproject.monadclient.recyclerviews;

import android.support.v7.widget.CardView;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.List;

import se.uu.csproject.monadclient.R;

public class NotificationRecyclerViewAdapter extends RecyclerView.Adapter<NotificationRecyclerViewAdapter.NotificationViewHolder> {

    public static class NotificationViewHolder extends RecyclerView.ViewHolder {

        CardView cv;
        TextView notificationName;
        TextView notificationTime;
        ImageView notificationPhoto;

        NotificationViewHolder(View itemView) {
            super(itemView);
            cv = (CardView)itemView.findViewById(R.id.cv);
            notificationName = (TextView)itemView.findViewById(R.id.text);
            notificationTime = (TextView)itemView.findViewById(R.id.time);
            notificationPhoto = (ImageView)itemView.findViewById(R.id.icon);
        }
    }

    List<Notify> notify;

    public NotificationRecyclerViewAdapter(List<Notify> notify){
        this.notify = notify;
    }

    @Override
    public void onAttachedToRecyclerView(RecyclerView recyclerView) {
        super.onAttachedToRecyclerView(recyclerView);
    }

    @Override
    public NotificationViewHolder onCreateViewHolder(ViewGroup viewGroup, int i) {
        View v = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.list_item_notification, viewGroup, false);
        NotificationViewHolder pvh = new NotificationViewHolder(v);
        return pvh;
    }

    @Override
    public void onBindViewHolder(NotificationViewHolder notificationViewHolder, int i) {
        notificationViewHolder.notificationName.setText(notify.get(i).name);
        notificationViewHolder.notificationTime.setText(notify.get(i).time);
        notificationViewHolder.notificationPhoto.setImageResource(notify.get(i).iconId);
    }

    @Override
    public int getItemCount() {
        return notify.size();
    }
}
