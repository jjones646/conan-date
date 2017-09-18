#include "date/date.h"
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <locale>
#include <ostream>
#include <stdexcept>
#include <string>

using namespace date;
using namespace std::chrono;

auto lprintdate = [](auto const & d) {std::cout << d << std::endl; };

int main()
{
    {
        sys_days d1 = 2016_y / oct / 29;
        sys_days d2 = 29_d / oct / 2016;
        sys_days d3 = oct / 29 / 2016;
        auto today = floor<days>(system_clock::now());
         
        lprintdate(d1);      // 2016-10-29
        lprintdate(d2);      // 2016-10-29
        lprintdate(d3);      // 2016-10-29
        lprintdate(today);   // 2016-10-31
    }
    {
        year_month_day d1 = 2016_y / oct / 29;
        year_month_day d2 = 29_d / oct / 2016;
        year_month_day d3 = oct / 29 / 2016;
        year_month_day today = floor<days>(system_clock::now());
         
        lprintdate(d1);      // 2016-10-29
        lprintdate(d2);      // 2016-10-29
        lprintdate(d3);      // 2016-10-29
        lprintdate(today);   // 2016-10-31
    }
    {
        auto wd1 = 2016_y / oct / mon[1];
        auto wd2 = mon[1] / oct / 2016;
        auto wd3 = oct / mon[1] / 2016;
         
        lprintdate(wd1);     // 2016/Oct/Mon[1]
        lprintdate(wd2);     // 2016/Oct/Mon[1]
        lprintdate(wd3);     // 2016/Oct/Mon[1]
         
        auto d1 = year_month_day{ wd1 };
        auto d2 = year_month_day{ wd2 };
        auto d3 = year_month_day{ wd2 };
         
        lprintdate(d1);      // 2016-10-03
        lprintdate(d2);      // 2016-10-03
        lprintdate(d3);      // 2016-10-03
    }
    {
        auto today = floor<days>(system_clock::now());
        auto tomorrow = today + days{ 1 };
        auto yesterday = today - days{ 1 };
         
        lprintdate(yesterday);  // 2016-10-30
        lprintdate(today);      // 2016-10-31
        lprintdate(tomorrow);   // 2016-11-01
    }
    {
        auto today = year_month_day{ floor<days>(system_clock::now()) };
        auto first_day_this_month = year_month_day{ today.year(), today.month(), day{ 1 } };
        lprintdate(first_day_this_month);// 2016-10-01
         
        auto d1 = year_month_day_last(today.year(), month_day_last{ today.month() });
        auto last_day_this_month = year_month_day{ d1 };
        lprintdate(last_day_this_month); // 2016-10-31
         
        auto d2 = year_month_day_last(year{ 2016 }, month_day_last{ month{ 2 } });
        auto last_day_feb = year_month_day{ d2 };
        lprintdate(last_day_feb);        // 2016-02-29
    }


    return 0;
}