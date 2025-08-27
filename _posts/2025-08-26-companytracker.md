---
layout: default
body_class: company-tracker-page
---

<!-- Company Tracker Dashboard -->
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
            .chart-container {
            position: relative;
            width: 100%;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            height: 300px;
            max-height: 400px;
        }
    @media (min-width: 768px) {
        .chart-container {
            height: 350px;
        }
    }
    .stat-card {
        background-color: #ffffff;
        border: 1px solid #f0e9e1;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    .filter-btn {
        transition: all 0.2s ease-in-out;
        border: 1px solid #dcdcdc;
    }
    .filter-btn.active {
        background-color: #8d7b68;
        color: #ffffff;
        border-color: #8d7b68;
    }
    .filter-btn:not(.active):hover {
        background-color: #f5f2ef;
    }
    .company-card {
        border: 1px solid #f0e9e1;
        transition: box-shadow 0.3s;
    }
    .company-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
</style>

<div class="company-tracker-dashboard" style="font-family: 'Inter', sans-serif; background-color: #fdfcfb; color: #3a3a3a;">
    <div class="w-full max-w-none mx-auto p-4 md:p-8">
    <header class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-4">Startup Trajectories & Personal Tastes: A Log of My 2017 Job Hunt</h1>
        <p class="text-lg text-gray-700 mb-4">I'm building a page to log all the companies I've marked over time. It's partly for fun, but also to explore a few bigger questions:</p>
        <div class="mb-4">
            <p class="text-base text-gray-700 mb-2"><strong>Company trajectories</strong> — what general patterns emerge in the growth or decline of startups and other companies?</p>
            <p class="text-base text-gray-700 mb-2"><strong>Personal choices</strong> — how have my own tastes and career priorities changed? And what if I had actually joined some of these companies?</p>
        </div>
        <p class="text-base text-gray-600 italic">
            This project was prompted while decluttering my old Apple Notes. I found a 2017 list of companies I had planned to apply to for internships or full-time roles during my Master's in Data Science at NYU. Curious, I decided to check how those companies are doing now. To make it more engaging, I asked ChatGPT/Gemini to help investigate their current status.
        </p>
    </header>

    <main>
        <section id="dashboard" class="mb-8 p-6 bg-white rounded-xl shadow-sm border border-gray-200">
            <div class="text-center mb-6">
                <h2 class="text-2xl font-semibold text-gray-800">Market Snapshot</h2>
                <!-- <p class="text-gray-500 mt-1">This section provides a high-level summary of the company statuses within the dataset. The chart and statistics below are interactive and will update as you apply filters to explore the data.</p> -->
            </div>
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
                    <div class="lg:col-span-1">
                        <div class="grid grid-cols-2 gap-4">
                        <div id="total-card" class="stat-card p-4 rounded-lg text-center">
                            <p class="text-sm text-gray-500">Total Companies</p>
                            <p id="total-count" class="text-3xl font-bold text-[#65451F]">0</p>
                        </div>
                        <div id="public-card" class="stat-card p-4 rounded-lg text-center">
                            <p class="text-sm text-gray-500">Public</p>
                            <p id="public-count" class="text-3xl font-bold text-green-600">0</p>
                        </div>
                        <div id="private-card" class="stat-card p-4 rounded-lg text-center">
                            <p class="text-sm text-gray-500">Private</p>
                            <p id="private-count" class="text-3xl font-bold text-blue-600">0</p>
                        </div>
                        <div id="acquired-card" class="stat-card p-4 rounded-lg text-center">
                            <p class="text-sm text-gray-500">Acquired/Integrated</p>
                            <p id="acquired-count" class="text-3xl font-bold text-purple-600">0</p>
                        </div>
                    </div>
                </div>
                <div class="lg:col-span-2">
                    <div class="chart-container">
                        <canvas id="statusChart"></canvas>
                    </div>
                </div>
            </div>
        </section>
        
        <section id="explorer" class="p-6 bg-white rounded-xl shadow-sm border border-gray-200">
            <div class="text-center mb-6">
                <h2 class="text-2xl font-semibold text-gray-800">Company Explorer</h2>
                <!-- <p class="text-gray-500 mt-1">Use the filters and search bar below to navigate the dataset. Selecting a status will update the summary above and refine the list of companies displayed, allowing you to focus on specific outcomes.</p> -->
            </div>
            <div class="flex flex-col md:flex-row gap-4 mb-6">
                <div class="relative flex-grow">
                    <input type="text" id="search-input" placeholder="Search by company name..." class="w-full p-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#a08c76] focus:border-transparent">
                    <svg class="w-5 h-5 text-gray-400 absolute top-1/2 left-3 -translate-y-1/2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </div>
                <div id="filter-controls" class="flex items-center justify-center gap-2 flex-wrap">
                    <button class="filter-btn active px-4 py-2 rounded-lg" data-filter="all">All</button>
                    <button class="filter-btn px-4 py-2 rounded-lg" data-filter="public">Public</button>
                    <button class="filter-btn px-4 py-2 rounded-lg" data-filter="private">Private</button>
                    <button class="filter-btn px-4 py-2 rounded-lg" data-filter="acquired">Acquired</button>
                </div>
            </div>

            <div id="company-list" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            </div>
                <p id="no-results" class="text-center text-gray-500 py-12 hidden">No companies match your criteria.</p>
        </section>
        
    </main>
</div>

<script>
    const companyData = [
        { company: "Precyse", trajectory: "Became part of MedAssets-Precyse → rebranded nThrive (2016) → FinThrive (2022).", status: "Operating as FinThrive (private).", category: "private" },
        { company: "Pinterest", trajectory: "Steady growth; bigger AI/commerce push; hit record users in 2025.", status: "Public (NYSE: PINS); 578M MAUs, +17% rev in Q2’25.", category: "public" },
        { company: "A9 (Amazon)", trajectory: "A9 brand retired; folded into Amazon Search; a9.com taken down in 2019.", status: "Functions as Amazon Search inside Amazon.", category: "acquired" },
        { company: "TripAdvisor", trajectory: "Pandemic trough → recovery; exploring separation of Viator/TheFork in 2025.", status: "Public; owns Viator & TheFork, evaluating separation.", category: "public" },
        { company: "GrassBridge LLC", trajectory: "Boutique tech recruiting firm (not a product company).", status: "Active recruiter.", category: "private" },
        { company: "Reflektion", trajectory: "Acquired by Sitecore in 2021.", status: "Part of Sitecore’s personalization stack.", category: "acquired" },
        { company: "Adobe", trajectory: "Killed the $20B Figma deal (Dec 2023); leaned harder into Firefly/AI.", status: "Public (ADBE); generative-AI a core focus.", category: "public" },
        { company: "Medallia", trajectory: "Taken private by Thoma Bravo (2021).", status: "Private under Thoma Bravo.", category: "private" },
        { company: "Skyhigh Networks", trajectory: "Acquired by McAfee (2018); relaunched as Skyhigh Security under STG (2022).", status: "Skyhigh Security operating privately.", category: "private" },
        { company: "Yelp", trajectory: "Continued steady, review-driven ad business through 2025.", status: "Public (YELP).", category: "public" },
        { company: "Groupon", trajectory: "Deep restructuring; “comeback” narrative in 2024–25.", status: "Public (GRPN).", category: "public" },
        { company: "Zensight", trajectory: "Acquired by Seismic (2018).", status: "Integrated into Seismic.", category: "acquired" },
        { company: "Indeed", trajectory: "Major layoffs in 2023 & 2024; in 2025 Recruit starts integrating Indeed & Glassdoor.", status: "Part of Recruit’s HR Tech unit; deeper Glassdoor tie-up.", category: "acquired" },
        { company: "Fitbit", trajectory: "Acquisition by Google closed Jan 2021.", status: "Google’s wearables brand.", category: "acquired" },
        { company: "Uber", trajectory: "IPO 2019; reached sustained GAAP profitability by 2024.", status: "Public (UBER), profitable platform.", category: "public" },
        { company: "Quantcast", trajectory: "Stayed private; multiple restructurings/layoffs in 2023–24.", status: "Private ad-tech firm.", category: "private" },
        { company: "ePlus", trajectory: "Kept compounding as an IT solutions VAR; strong FY25 prints.", status: "Public (PLUS).", category: "public" },
        { company: "eHarmony", trajectory: "Acquired by Germany’s Parship/Elite Group (2018).", status: "Part of ParshipMeet Group.", category: "acquired" },
        { company: "Lynx (Analytics)", trajectory: "Continued as a telco-focused analytics company.", status: "Private; active in APAC.", category: "private" },
        { company: "Adap.tv", trajectory: "Already part of AOL (pre-2017); AOL/Yahoo sold to Apollo in 2021.", status: "Within Yahoo’s ad-tech history; brand long sunset.", category: "acquired" },
        { company: "OnDeck", trajectory: "Acquired by Enova (2020).", status: "Brand within Enova.", category: "acquired" },
        { company: "Facebook", trajectory: "Rebranded to Meta (2021).", status: "Public (META).", category: "public" },
        { company: "IBM (Watson team)", trajectory: "Sold Watson Health → Merative (2022); launched watsonx (2023).", status: "IBM focuses Watsonx + enterprise AI.", category: "acquired" },
        { company: "Quora", trajectory: "Launched AI platform Poe (public in 2023; API 2025).", status: "Private; running Quora + Poe.", category: "private" },
        { company: "Airbnb", trajectory: "IPO in 2020; profitable at scale by 2023–24.", status: "Public (ABNB).", category: "public" },
        { company: "Twitter → X", trajectory: "Acquired by Elon Musk (Oct 2022); rebranded to X; HQ moved to TX (2024).", status: "Private under X Corp.", category: "private" },
        { company: "Coursera", trajectory: "IPO in 2021 (NYSE: COUR).", status: "Public ed-tech platform.", category: "public" },
        { company: "Glassdoor", trajectory: "Acquired by Recruit (2018); 2025 integration moves with Indeed.", status: "Under Recruit’s HR Tech; tighter Indeed pairing.", category: "acquired" },
        { company: "Bloomreach", trajectory: "Acquired Exponea (2021) + $150M raise.", status: "Private commerce-experience platform.", category: "private" },
        { company: "Zillow", trajectory: "Wound down iBuying (2021) then refocused; Q2’25 beat.", status: "Public (Z, ZG); profitable adj. EBITDA in Q2’25.", category: "public" },
        { company: "Meetup", trajectory: "Bought by WeWork (2017), sold to AlleyCorp-led group (2020).", status: "Private, independent of WeWork.", category: "private" },
        { company: "DataRobot", trajectory: "Leadership turmoil 2022; pivoted to gen-AI suite in 2024.", status: "Private, enterprise-AI apps/agents.", category: "private" },
        { company: "AOL", trajectory: "Verizon sold Yahoo/AOL to Apollo; now inside Yahoo (2021).", status: "Legacy brand under Yahoo/Apollo.", category: "acquired" },
        { company: "Wealthfront", trajectory: "UBS–Wealthfront acquisition terminated (Sept 2022); stayed independent.", status: "Private robo-advisor.", category: "private" },
        { company: "Palantir", trajectory: "Direct-listed on NYSE in 2020; scaled gov/commercial AI.", status: "Public (PLTR).", category: "public" },
        { company: "Heap", trajectory: "Acquired by Contentsquare (deal closed Dec 2023).", status: "Part of Contentsquare.", category: "acquired" },
        { company: "Apple (Siri teams)", trajectory: "Announced “Apple Intelligence” (WWDC 2024) with a big Siri upgrade; expanded 2025.", status: "Public (AAPL); rolling out Apple Intelligence.", category: "public" },
        { company: "Kosei", trajectory: "Pinterest acquired Kosei (2015) for ML recommendations.", status: "Tech long integrated at Pinterest.", category: "acquired" },
        { company: "Rocket Fuel", trajectory: "Bought by Sizmek (2017); Amazon acquired Sizmek’s ad server/DCO in 2019.", status: "Rocket Fuel brand gone; pieces live inside Amazon Advertising & others.", category: "acquired" },
        { company: "Google", trajectory: "Continued as Alphabet; search/ads + cloud + devices expansion.", status: "Public (GOOGL).", category: "public" },
        { company: "Aetna", trajectory: "CVS Health completed acquisition (Nov 2018).", status: "CVS subsidiary.", category: "acquired" },
        { company: "Trulia", trajectory: "Acquired by Zillow (2015); brand kept within Zillow Group.", status: "Part of Zillow Group.", category: "acquired" },
        { company: "Apple (Maps eval)", trajectory: "Same Apple trajectory as above.", status: "Public (AAPL).", category: "public" },
        { company: "American Express", trajectory: "Steady financials, brand strength through 2025.", status: "Public (AXP).", category: "public" },
        { company: "Travelport", trajectory: "Taken private by Siris/Evergreen (deal closed 2019).", status: "Private travel-tech GDS.", category: "private" },
        { company: "Sandia (Nat’l Labs)", trajectory: "Ongoing DOE/NNSA mission; run by NTESS (Honeywell subsidiary).", status: "Active U.S. national lab.", category: "private" }
    ];

    const companyList = document.getElementById('company-list');
    const searchInput = document.getElementById('search-input');
    const filterControls = document.getElementById('filter-controls');
    const noResults = document.getElementById('no-results');

    let statusChart;
    let currentFilter = 'all';

    const categoryColors = {
        public: 'rgb(22 163 74)',
        private: 'rgb(37 99 235)',
        acquired: 'rgb(124 58 237)',
    };

    const getStatusCategory = (statusText) => {
        const lowerStatus = statusText.toLowerCase();
        if (lowerStatus.includes('public') || lowerStatus.includes('(nyse:') || lowerStatus.includes('(nasdaq:') || lowerStatus.includes('(adbe)') || lowerStatus.includes('(yelp)') || lowerStatus.includes('(grpn)') || lowerStatus.includes('(uber)') || lowerStatus.includes('(plus)') || lowerStatus.includes('(meta)') || lowerStatus.includes('(abnb)') || lowerStatus.includes('(pltr)') || lowerStatus.includes('(aapl)') || lowerStatus.includes('(googl)') || lowerStatus.includes('(axp)') || lowerStatus.includes('(z, zg)')) {
            return 'public';
        }
        if (lowerStatus.includes('private') || lowerStatus.includes('recruiter') || lowerStatus.includes('independent') || lowerStatus.includes('national lab')) {
            return 'private';
        }
        return 'acquired';
    };

    const dataWithCategories = companyData.map(c => ({ ...c, category: getStatusCategory(c.status) }));

    const renderCompanyList = (data) => {
        companyList.innerHTML = '';
        if (data.length === 0) {
            noResults.classList.remove('hidden');
        } else {
            noResults.classList.add('hidden');
        }
        data.forEach(company => {
            const card = document.createElement('div');
            card.className = 'company-card bg-white p-5 rounded-lg shadow-sm';
            
            let statusColorClass = '';
            let statusBgClass = '';
            switch (company.category) {
                case 'public':
                    statusColorClass = 'text-green-800';
                    statusBgClass = 'bg-green-100';
                    break;
                case 'private':
                    statusColorClass = 'text-blue-800';
                    statusBgClass = 'bg-blue-100';
                    break;
                case 'acquired':
                    statusColorClass = 'text-purple-800';
                    statusBgClass = 'bg-purple-100';
                    break;
            }

            card.innerHTML = `
                <div class="flex justify-between items-start">
                    <h3 class="text-xl font-bold text-gray-800 mb-2">${company.company}</h3>
                    <span class="text-xs font-semibold px-2 py-1 rounded-full ${statusColorClass} ${statusBgClass}">${company.category.charAt(0).toUpperCase() + company.category.slice(1)}</span>
                </div>
                <p class="text-sm text-gray-600 mb-3"><span class="font-semibold">Trajectory:</span> ${company.trajectory}</p>
                <p class="text-sm text-gray-600"><span class="font-semibold">2025 Status:</span> ${company.status}</p>
            `;
            companyList.appendChild(card);
        });
    };

    const updateStats = (data) => {
        const total = data.length;
        const publicCount = data.filter(c => c.category === 'public').length;
        const privateCount = data.filter(c => c.category === 'private').length;
        const acquiredCount = data.filter(c => c.category === 'acquired').length;

        document.getElementById('total-count').textContent = total;
        document.getElementById('public-count').textContent = publicCount;
        document.getElementById('private-count').textContent = privateCount;
        document.getElementById('acquired-count').textContent = acquiredCount;
    };

    const updateChart = (data) => {
        const publicCount = data.filter(c => c.category === 'public').length;
        const privateCount = data.filter(c => c.category === 'private').length;
        const acquiredCount = data.filter(c => c.category === 'acquired').length;

        if (statusChart) {
            statusChart.data.datasets[0].data = [publicCount, privateCount, acquiredCount];
            statusChart.update();
        }
    };

    const filterAndRender = () => {
        const searchTerm = searchInput.value.toLowerCase();
        let filteredData = dataWithCategories;

        if (currentFilter !== 'all') {
            filteredData = filteredData.filter(c => c.category === currentFilter);
        }

        if (searchTerm) {
            filteredData = filteredData.filter(c => c.company.toLowerCase().includes(searchTerm));
        }

        renderCompanyList(filteredData);
        updateStats(filteredData);
        updateChart(filteredData);
    };

    const initializeChart = () => {
        const ctx = document.getElementById('statusChart').getContext('2d');
        const publicCount = dataWithCategories.filter(c => c.category === 'public').length;
        const privateCount = dataWithCategories.filter(c => c.category === 'private').length;
        const acquiredCount = dataWithCategories.filter(c => c.category === 'acquired').length;

        statusChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Public', 'Private', 'Acquired/Integrated'],
                datasets: [{
                    label: 'Company Status',
                    data: [publicCount, privateCount, acquiredCount],
                    backgroundColor: [
                        categoryColors.public,
                        categoryColors.private,
                        categoryColors.acquired,
                    ],
                    borderColor: '#fdfcfb',
                    borderWidth: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                size: 14,
                                family: 'Inter'
                            },
                            color: '#3a3a3a'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed !== null) {
                                    label += context.parsed;
                                }
                                return label;
                            }
                        }
                    }
                },
                cutout: '60%'
            }
        });
    };

    document.addEventListener('DOMContentLoaded', () => {
        renderCompanyList(dataWithCategories);
        updateStats(dataWithCategories);
        initializeChart();

        searchInput.addEventListener('input', filterAndRender);

        filterControls.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON') {
                currentFilter = e.target.dataset.filter;
                document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
                e.target.classList.add('active');
                filterAndRender();
            }
        });
    });
</script>
</div>
