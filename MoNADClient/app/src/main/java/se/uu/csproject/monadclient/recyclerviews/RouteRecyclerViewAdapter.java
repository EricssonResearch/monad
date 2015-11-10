//package se.uu.csproject.monadclient.recyclerviews;
//
//import android.support.v7.widget.RecyclerView;
//import android.view.LayoutInflater;
//import android.view.View;
//import android.view.ViewGroup;
//import android.widget.ImageView;
//import android.widget.TextView;
//
//import java.util.List;
//
//import se.uu.csproject.monadclient.R;
//
//public class RouteRecyclerViewAdapter extends RecyclerView.Adapter<RouteRecyclerViewAdapter.BusstopsViewHolder> {
//
//    public static class BusstopsViewHolder extends RecyclerView.ViewHolder {
//
//
//        TextView busstopName;
//        TextView busstopTime;
//        ImageView busstopPhoto;
//
//
//        BusstopsViewHolder(View itemView) {
//            super(itemView);
//
//            busstopName = (TextView)itemView.findViewById(R.id.text1);
//            busstopTime = (TextView)itemView.findViewById(R.id.time2);
//            busstopPhoto = (ImageView)itemView.findViewById(R.id.bus3);
//        }
//    }
//
//    List<Notify> notify;
//
//    public RouteRecyclerViewAdapter(List<Notify> notify){
//        this.notify = notify;
//    }
//
//    @Override
//    public void onAttachedToRecyclerView(RecyclerView recyclerView) {
//        super.onAttachedToRecyclerView(recyclerView);
//    }
//
//    @Override
//    public BusstopsViewHolder onCreateViewHolder(ViewGroup viewGroup, int i) {
//        View v = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.list_item_busstop, viewGroup, false);
//        BusstopsViewHolder bst = new BusstopsViewHolder(v);
//        return bst;
//
//    }
//
//    @Override
//    public void onBindViewHolder(BusstopsViewHolder busstopsViewHolder, int i) {
//        busstopsViewHolder.busstopName.setText(notify.get(i).text);
////        busstopsViewHolder.busstopTime.setText(notify.get(i).time);
//        busstopsViewHolder.busstopPhoto.setImageResource(notify.get(i).iconID);
//    }
//
//    @Override
//    public int getItemCount() {
//        return notify.size();
//    }
//}
//
//
//
