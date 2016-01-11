#!/bin/bash

function press_enter
{
    echo ""
    echo -n "Press Enter to continue"
    read
    clear
}

selection=
until [ "$selection" = "0" ]; do
    echo "---------------------------------------------------------------------------------------------------------"
    echo "|                                               TESTS MENU                                              |"
    echo "|-------------------------------------------------------------------------------------------------------|"
    echo "| 1 - Only two clusters, Flogsta -> Polacksbacken and Polacksbacken -> Flogsta.                         |"
    echo "|                                                                                                       |"
    echo "| 2 - No duplicates, only 1 route.                                                                      |"
    echo "|                                                                                                       |"
    echo "| 3 - Three clusters, Flogsta -> Polacksbacken, Polacksbacken -> Flogsta, Granby -> Gamla Uppsala.      |"
    echo "|                                                                                                       |"
    echo "| 4 - Same three clusters plus random data.                                                             |"
    echo "|                                                                                                       |"
    echo "| 5 - Same two clusters as before, plus Granby -> Polacksbacken. Best match is Gamla -> Polacksbacken.  |"
    echo "|                                                                                                       |"
    echo "| 6 - Two clusters same as before but random routes. 1000 requests and 1000 routes to compare with.     |"
    echo "|                                                                                                       |"
    echo "| 0 - Exit program.                                                                                     |"
    echo "---------------------------------------------------------------------------------------------------------"
    echo -n "Enter selection: "
    read selection
    echo ""
    case $selection in
        1 ) #python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/case1_requests.py;
            #python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/case1_timetable.py;
            /home/babis/Applications/spark-1.5.0/bin/spark-submit /home/babis/Desktop/MoNAD/monad/TravelRecommendation/TravelRecommendation.py;
            python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/empty_mongoDB.py;
            press_enter ;;
        2 ) python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/case2_requests.py;
            python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/case2_timetable.py;
            /home/babis/Applications/spark-1.5.0/bin/spark-submit /home/babis/Desktop/MoNAD/monad/TravelRecommendation/TravelRecommendation.py;
            python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/empty_mongoDB.py;
            press_enter ;;
        3 ) python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/case3_requests.py;
            python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/case3_timetable.py;
            /home/babis/Applications/spark-1.5.0/bin/spark-submit /home/babis/Desktop/MoNAD/monad/TravelRecommendation/TravelRecommendation.py;
            python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/empty_mongoDB.py;
            press_enter ;;
        4 ) python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/case4_requests.py;
            python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/case4_timetable.py;
            /home/babis/Applications/spark-1.5.0/bin/spark-submit /home/babis/Desktop/MoNAD/monad/TravelRecommendation/TravelRecommendation.py;
            python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/empty_mongoDB.py;
            press_enter ;;
        5 ) python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/case5_requests.py;
            python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/case5_timetable.py;
            /home/babis/Applications/spark-1.5.0/bin/spark-submit /home/babis/Desktop/MoNAD/monad/TravelRecommendation/TravelRecommendation.py;
            python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/empty_mongoDB.py;
            press_enter ;;
        6 ) python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/case6_requests.py;
            python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/case6_timetable.py;
            /home/babis/Applications/spark-1.5.0/bin/spark-submit /home/babis/Desktop/MoNAD/monad/TravelRecommendation/TravelRecommendation.py;
            python /home/babis/Desktop/MoNAD/monad/TravelRecommendation/empty_mongoDB.py;
            press_enter ;;
        0 ) exit ;;
        * ) echo "Please enter 1, 2, 3, 4, 5, 6 or 0"; press_enter
    esac
done




#/home/babis/Applications/spark-1.5.0/bin/spark-submit
/home/babis/Desktop/MoNAD/monad/TravelRecommendation/TravelRecommendation.py
