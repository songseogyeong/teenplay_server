// fetch로 각 탭에 해당하는 정보 가져오는 함수
const clubDetailService = (() => {
    const getClubMemberInfo = async (memberId, clubId, callback) => {
        let url = `/clubs/club-member/api/${memberId}/${clubId}`
        const response = await fetch(url);
        const clubMembers = await response.json();

        await callback(clubMembers)
    }

    const getOngoingActivityList = async (clubId, callback) => {
        const url = `/clubs/club-ongoing-activity/api/${clubId}`
        const response = await fetch(url)
        const ongoingActivities = await response.json()

        return callback(ongoingActivities);
    }

    const getFinishedActivityList = async (clubId, page, callback) => {
        const url = `/clubs/club-finished-activity/api/${clubId}/${page}`
        const response = await fetch(url)
        const finishedActivities = await response.json()

        if (callback){
            return callback(finishedActivities)
        }
        return finishedActivities
    }

    const getClubNotices = async (clubId, page, callback) => {
        const url = `/clubs/club-notice/api/${clubId}/${page}`
        const response = await fetch(url)
        const clubNotices = await response.json()

        if (callback) {
            return callback(clubNotices)
        }
        return clubNotices
    }

    const getTeenplayList = async () => {}

    const updateClubMemberStatus = async (memberId, clubId) => {
        await fetch(`/clubs/club-member/api/${memberId}/${clubId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
            // body: JSON.stringify({'club_id': clubId, 'member_id': memberId})
        });

        await getClubMemberInfo(memberId, clubId, createClubTopBtn);
    }

    const updateActivityLike = async (activityId, isCreate) => {
        console.log(activityId)
        console.log(isCreate)
        await fetch(`/activity/like?id=${activityId}&is-create=${isCreate}`);
    }

    return {
        getCMInfo: getClubMemberInfo,
        getOAList: getOngoingActivityList,
        getFAList: getFinishedActivityList,
        getCNList: getClubNotices,
        getTPList: getTeenplayList,
        updateCMStatus: updateClubMemberStatus,
        updateActivityLike: updateActivityLike,
    }
})()