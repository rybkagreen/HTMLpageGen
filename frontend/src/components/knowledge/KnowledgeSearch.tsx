import { Document, KnowledgeBase, SearchResult } from '@/lib/knowledge-base';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import {
  Brain,
  ChevronRight,
  ExternalLink,
  Lightbulb,
  Search,
  Star,
  Tag,
  TrendingUp,
} from 'lucide-react';
import { memo, useEffect, useState } from 'react';

interface KnowledgeSearchProps {
  knowledgeBase: KnowledgeBase;
  onSuggestionSelect: (content: string) => void;
  className?: string;
}

const KnowledgeSearch = memo(function KnowledgeSearch({
  knowledgeBase,
  onSuggestionSelect,
  className,
}: KnowledgeSearchProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [recommendations, setRecommendations] = useState<Document[]>([]);
  const [popularTopics, setPopularTopics] = useState<string[]>([]);

  useEffect(() => {
    loadRecommendations();
    loadPopularTopics();
  }, []);

  useEffect(() => {
    if (searchQuery.length >= 2) {
      performSearch(searchQuery);
    } else {
      setSearchResults([]);
    }
  }, [searchQuery]);

  const performSearch = async (query: string) => {
    setIsSearching(true);
    try {
      const results = await knowledgeBase.search(query, 6);
      setSearchResults(results);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const loadRecommendations = async () => {
    const recs = await knowledgeBase.getRecommendations({});
    setRecommendations(recs.slice(0, 4));
  };

  const loadPopularTopics = () => {
    const topics = [
      'responsive design',
      'flexbox layout',
      'dark theme',
      'animations',
      'accessibility',
      'performance',
    ];
    setPopularTopics(topics);
  };

  const handleSuggestionClick = (content: string) => {
    onSuggestionSelect(content);
    knowledgeBase.recordUsage(content);
  };

  const formatCategory = (category: string) => {
    return category.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <motion.div
      className={cn('bg-gray-50 dark:bg-gray-900 rounded-lg p-4', className)}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Заголовок */}
      <div className='flex items-center mb-4'>
        <Brain className='h-5 w-5 text-blue-600 mr-2' />
        <h3 className='text-lg font-semibold text-gray-900 dark:text-white'>
          База знаний
        </h3>
      </div>

      {/* Поиск */}
      <div className='relative mb-4'>
        <Search className='absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400' />
        <input
          type='text'
          placeholder='Поиск по базе знаний...'
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          className='w-full pl-10 pr-4 py-2 border border-gray-200 dark:border-gray-700 rounded-lg 
                   bg-white dark:bg-gray-800 text-gray-900 dark:text-white 
                   focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all'
        />
        {isSearching && (
          <div className='absolute right-3 top-1/2 transform -translate-y-1/2'>
            <div className='animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full' />
          </div>
        )}
      </div>

      {/* Результаты поиска */}
      {searchResults.length > 0 && (
        <motion.div
          className='mb-4'
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.2 }}
        >
          <h4 className='text-sm font-medium text-gray-700 dark:text-gray-300 mb-2'>
            Результаты поиска
          </h4>
          <div className='space-y-2 max-h-40 overflow-y-auto'>
            {searchResults.map((result, index) => (
              <motion.div
                key={result.document.id}
                className='p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 
                         hover:shadow-sm cursor-pointer transition-all'
                onClick={() => handleSuggestionClick(result.document.content)}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.2, delay: index * 0.05 }}
              >
                <div className='flex items-start justify-between'>
                  <div className='flex-1'>
                    <div className='flex items-center mb-1'>
                      <h5 className='text-sm font-medium text-gray-900 dark:text-white'>
                        {result.document.title}
                      </h5>
                      <span
                        className='ml-2 px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900 
                                   text-blue-700 dark:text-blue-300 rounded-full'
                      >
                        {formatCategory(result.document.category)}
                      </span>
                    </div>
                    <p className='text-xs text-gray-600 dark:text-gray-400 line-clamp-2'>
                      {result.relevantChunks[0] ||
                        result.document.content.substring(0, 120)}
                      ...
                    </p>
                    <div className='flex items-center mt-2'>
                      <Star className='h-3 w-3 text-yellow-500 mr-1' />
                      <span className='text-xs text-gray-500'>
                        {Math.round(result.similarity * 100)}% совпадение
                      </span>
                    </div>
                  </div>
                  <ChevronRight className='h-4 w-4 text-gray-400' />
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Рекомендации */}
      {searchQuery.length === 0 && recommendations.length > 0 && (
        <motion.div
          className='mb-4'
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
        >
          <div className='flex items-center mb-2'>
            <Lightbulb className='h-4 w-4 text-yellow-500 mr-2' />
            <h4 className='text-sm font-medium text-gray-700 dark:text-gray-300'>
              Рекомендации
            </h4>
          </div>
          <div className='grid grid-cols-1 gap-2'>
            {recommendations.map((doc, index) => (
              <motion.div
                key={doc.id}
                className='p-2 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 
                         hover:shadow-sm cursor-pointer transition-all'
                onClick={() => handleSuggestionClick(doc.content)}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2, delay: index * 0.1 }}
              >
                <div className='flex items-center justify-between'>
                  <div className='flex-1'>
                    <h5 className='text-sm font-medium text-gray-900 dark:text-white mb-1'>
                      {doc.title}
                    </h5>
                    <div className='flex items-center'>
                      {doc.tags.slice(0, 2).map(tag => (
                        <span
                          key={tag}
                          className='mr-1 px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 
                                   text-gray-600 dark:text-gray-400 rounded-full'
                        >
                          {tag}
                        </span>
                      ))}
                      {doc.useCount > 0 && (
                        <div className='flex items-center ml-2'>
                          <TrendingUp className='h-3 w-3 text-green-500 mr-1' />
                          <span className='text-xs text-green-600 dark:text-green-400'>
                            {doc.useCount}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                  <ExternalLink className='h-3 w-3 text-gray-400' />
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Популярные темы */}
      {searchQuery.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          <div className='flex items-center mb-2'>
            <Tag className='h-4 w-4 text-purple-500 mr-2' />
            <h4 className='text-sm font-medium text-gray-700 dark:text-gray-300'>
              Популярные темы
            </h4>
          </div>
          <div className='flex flex-wrap gap-2'>
            {popularTopics.map((topic, index) => (
              <motion.button
                key={topic}
                className='px-3 py-1 text-xs bg-purple-100 dark:bg-purple-900 
                         text-purple-700 dark:text-purple-300 rounded-full 
                         hover:bg-purple-200 dark:hover:bg-purple-800 
                         transition-colors cursor-pointer'
                onClick={() => setSearchQuery(topic)}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.2, delay: index * 0.05 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {topic}
              </motion.button>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
});

export default KnowledgeSearch;
