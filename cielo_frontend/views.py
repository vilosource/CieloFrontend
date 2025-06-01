from django.shortcuts import render

def index(request):
    """
    Index view that displays the main dashboard/home page.
    """
    context = {
        'page_title': 'Dashboard',
        'cielo_navigation_items': [
            {
                'label': 'Dashboard',
                'url': '/',
                'icon_class': 'mdi mdi-view-dashboard-outline'
            },
            {
                'label': 'Infrastructure',
                'icon_class': 'mdi mdi-server-network',
                'sub_items': [
                    {
                        'label': 'Virtual Machines',
                        'url': '#',
                        'icon_class': 'mdi mdi-server'
                    },
                    {
                        'label': 'Storage',
                        'url': '#',
                        'icon_class': 'mdi mdi-database'
                    },
                    {
                        'label': 'Networks',
                        'url': '#',
                        'icon_class': 'mdi mdi-network'
                    }
                ]
            },
            {
                'label': 'Cloud Services',
                'icon_class': 'mdi mdi-cloud',
                'sub_items': [
                    {
                        'label': 'Azure Resources',
                        'icon_class': 'mdi mdi-microsoft-azure',
                        'sub_items': [
                            {
                                'label': 'Resource Groups',
                                'url': '#',
                                'icon_class': 'mdi mdi-folder-multiple'
                            },
                            {
                                'label': 'App Services',
                                'url': '#',
                                'icon_class': 'mdi mdi-application'
                            },
                            {
                                'label': 'SQL Databases',
                                'url': '#',
                                'icon_class': 'mdi mdi-database-plus'
                            },
                            {
                                'label': 'Key Vaults',
                                'url': '#',
                                'icon_class': 'mdi mdi-key'
                            }
                        ]
                    },
                    {
                        'label': 'Containers',
                        'url': '#',
                        'icon_class': 'mdi mdi-docker'
                    },
                    {
                        'label': 'Functions',
                        'url': '#',
                        'icon_class': 'mdi mdi-function'
                    }
                ]
            },
            {
                'label': 'Monitoring',
                'icon_class': 'mdi mdi-monitor-dashboard',
                'sub_items': [
                    {
                        'label': 'Alerts',
                        'url': '#',
                        'icon_class': 'mdi mdi-alert-circle'
                    },
                    {
                        'label': 'Metrics',
                        'url': '#',
                        'icon_class': 'mdi mdi-chart-line'
                    },
                    {
                        'label': 'Logs',
                        'url': '#',
                        'icon_class': 'mdi mdi-file-document-multiple'
                    }
                ]
            },
            {
                'label': 'Security',
                'icon_class': 'mdi mdi-shield-check',
                'sub_items': [
                    {
                        'label': 'Access Control',
                        'icon_class': 'mdi mdi-account-lock',
                        'sub_items': [
                            {
                                'label': 'Users',
                                'url': '#',
                                'icon_class': 'mdi mdi-account-multiple'
                            },
                            {
                                'label': 'Roles',
                                'url': '#',
                                'icon_class': 'mdi mdi-account-key'
                            },
                            {
                                'label': 'Permissions',
                                'url': '#',
                                'icon_class': 'mdi mdi-lock'
                            }
                        ]
                    },
                    {
                        'label': 'Compliance',
                        'url': '#',
                        'icon_class': 'mdi mdi-clipboard-check'
                    },
                    {
                        'label': 'Audit Logs',
                        'url': '#',
                        'icon_class': 'mdi mdi-file-search'
                    }
                ]
            },
            {
                'label': 'Administration',
                'icon_class': 'mdi mdi-cog',
                'sub_items': [
                    {
                        'label': 'User Management',
                        'url': '/users/profile/',
                        'icon_class': 'mdi mdi-account-circle'
                    },
                    {
                        'label': 'System Settings',
                        'url': '#',
                        'icon_class': 'mdi mdi-cog-outline'
                    },
                    {
                        'label': 'Backup & Recovery',
                        'url': '#',
                        'icon_class': 'mdi mdi-backup-restore'
                    }
                ]
            },
            {
                'label': 'Account',
                'icon_class': 'mdi mdi-account',
                'sub_items': [
                    {
                        'label': 'Profile',
                        'url': '/users/profile/',
                        'icon_class': 'mdi mdi-account-circle'
                    },
                    {
                        'label': 'Change Password',
                        'url': '/users/change-password/',
                        'icon_class': 'mdi mdi-lock-reset'
                    },
                    {
                        'label': 'Logout',
                        'url': '/users/logout/',
                        'icon_class': 'mdi mdi-logout'
                    }
                ]
            }
        ]
    }
    return render(request, 'index.html', context)