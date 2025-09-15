import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MainFeed from './MainFeed';
import TagsSidebar from './TagsSidebar';

const HomePage = () => {
    const [posts, setPosts] = useState([]);
    const [tags, setTags] = useState([]);

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await axios.get('/api/posts');
                setPosts(response.data);
            } catch (error) {
                console.error('Error fetching posts:', error);
            }
        };

        const fetchTags = async () => {
            try {
                const response = await axios.get('/api/tags');
                setTags(response.data);
            } catch (error) {
                console.error('Error fetching tags:', error);
            }
        };

        fetchPosts();
        fetchTags();
    }, []);

    return (
        <>
            <MainFeed posts={posts} />
            <TagsSidebar tags={tags} />
        </>
    );
};

export default HomePage;
