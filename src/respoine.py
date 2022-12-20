{
        "reporttype": "Ranking Report",
        "reportrank": "# Loans",
        "reportformat": "HTML",
        "usecode": {
                "id": 3,
                "usecodegroup": "RES",
                "usecode": "1-Family",
                "_uiSelectChoiceDisabled": False
        },
        "loanpurpose": "Purchase",
        "lendertype": "Banks",
        "lenderstodisplay": "5",
        "lenders": [],
        "ltext": "",
        "loantypes": "Conforming",
        "loantypessub": [
                "FHA"
        ],
        "refionly": True,
        "excl_usahud": True,
        "loantypessubbypass": True,
        "loanmin": "1",
        "loanmax": "2222",
        "summarizeby": "State Level",
        "allowcustomregion": True,
        "customregion": True,
        "state": [
                {
                        "state": "AK",
                        "_uiSelectChoiceDisabled": False
                }
        ],
        "county": [],
        "citytown": [],
        "zipcode": [],
        "censustract": [],
        "year": [
                "2021"
        ],
        "period": [
                "Q1"
        ],
        "reporting": {},
        "lt": {
                "lendertypesetup": True
        },
        "brokerlenderbypass": True,
        "uid": 196,
        "lenderflag": null,
        "lenderlen": 0,
        "ifilter": " AND ((mHMEQ = 'F') and (mHELOC = 'F')) AND (mLenderName != 'USA Housing and Urban Development')",
        "brokerflaginside": True,
        "report_ary": [
                [
                        [
                                "(All Other Lenders)",
                                "",
                                "",
                                "",
                                "$ 0",
                                "0",
                                "$0",
                                "0",
                                "$0",
                                "0",
                                "nan%",
                                "nan%",
                                "nan%"
                        ],
                        [
                                "All",
                                "",
                                "",
                                "",
                                "$0",
                                "0",
                                "$0",
                                "0",
                                "$0",
                                "0",
                                "100%",
                                "100%",
                                "100%"
                        ]
                ]
        ],
        "reportheader_ary": [
                [
                        "RES - 1-Family - by Broker Name",
                        "Skyward Techno.",
                        "All Regions in AK",
                        "2021 Q1",
                        "# Loans",
                        "12-09-2022 6:36AM"
                ]
        ],
        "brokerflag": True,
        "sql": [
                "select mBrokerName as mLenderName, TotalPurchaseAmount, NumPurchaseLoans, TotalNonPurchaseAmount, NumNonPurchaseLoans, (TotalPurchaseAmount + TotalNonPurchaseAmount) as TotalAmount, (NumPurchaseLoans + NumNonPurchaseLoans) as NumLoans from ( select mBrokerName, SUM(if (((mLoanUse = 'PMM')), mAmount, 0)) as TotalPurchaseAmount, SUM(if (((mLoanUse = 'PMM')), 1, 0)) as NumPurchaseLoans, SUM(if (((mLoanUse = 'OTH')  AND ((mHMEQ = 'F') and (mHELOC = 'F')) AND (mLenderName != 'USA Housing and Urban Development') ), mAmount, 0)) as TotalNonPurchaseAmount, SUM(if (((mLoanUse = 'OTH')  AND ((mHMEQ = 'F') and (mHELOC = 'F')) AND (mLenderName != 'USA Housing and Urban Development') ), 1, 0)) as NumNonPurchaseLoans from mortgage  where mPropType = 'RES' and mPropSubTP = '1-Family' and mCONFORMING = 'T' and (mFHA = 'T') and mAmount >= 1 and mAmount < 2222 and mAmount < 998999999 and ( mState = 'AK') and mYear = 2021 and mQuarter = 1 and mBrokerName <> '' and mBrokerName <> 'NONE' and mBrokerID <> '' group by mBrokerName with rollup) as totalTable where (NumPurchaseLoans + NumNonPurchaseLoans) > 0 order by NumPurchaseLoans desc, TotalPurchaseAmount desc, mLenderName;"
        ],
        "report": "<div class=\"reportblock\"><table class='msm_report_header'><tr><th width='75%' class='rpthd1'>RES - 1-Family - by Broker Name - Mortgage Marketshare Report</th><th width='25%' class='rpthd2'>2021 Q1</th></tr><tr><th class='rpthd3'>All Regions in AK</th><th class='reporttime'>Report Time: 12-09-2022 6:36AM</th></tr><tr><th class='rpthd4' colspan='2'>Rank by # Loans</th></tr></table><table class='msm_report'><tr class='subheader'><th colspan='4'>&nbsp;</th><th colspan='2' class='rptshd2'>All Mortgages</th><th colspan='2' class='rptshd3'>Purchase Mortgages</th><th colspan='2' class='rptshd4'>Non Purchase Mortgages</th><th colspan='3' class='rptshd5'>Mkt Shr by # Loans (%)</th></tr><tr class='subheader'><th>Broker Name</th><th>All</th><th>P</th><th>N</th><th>Total<br/>Value</th><th>Total<br/>Number</th><th>Total<br/>Value</th><th>Total<br/>Number</th><th>Total<br/>Value</th><th>Total<br/>Number</th><th>All</th><th>P</th><th>NP</th></tr><tr class='OtherBrokers'><td>(All Other Lenders)</td><td></td><td></td><td></td><td>$ 0</td><td>0</td><td>$0</td><td>0</td><td>$0</td><td>0</td><td>nan%</td><td>nan%</td><td>nan%</td></tr><tr class='Totals'><td>All</td><td></td><td></td><td></td><td>$0</td><td>0</td><td>$0</td><td>0</td><td>$0</td><td>0</td><td>100%</td><td>100%</td><td>100%</td></tr></table><p></p></div>"
}